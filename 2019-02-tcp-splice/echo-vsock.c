#define _GNU_SOURCE /* POLLRDHUP */

#include <arpa/inet.h>
#include <errno.h>
#include <linux/bpf.h>
#include <linux/tcp.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <sys/resource.h>
#include <time.h>
#include <unistd.h>
#include <sys/un.h>

#include "common.h"
#include "tbpf.h"

extern size_t bpf_insn_prog_parser_cnt;
extern struct bpf_insn bpf_insn_prog_parser[];
extern struct tbpf_reloc bpf_reloc_prog_parser[];

extern size_t bpf_insn_prog_verdict_cnt;
extern struct bpf_insn bpf_insn_prog_verdict[];
extern struct tbpf_reloc bpf_reloc_prog_verdict[];

static void usage(char *prog)
{
	fprintf(stderr, "Usage: %s <connect:port> [OPTIONS]\n", prog);
	fprintf(stderr, "\n");
	fprintf(stderr, "Create an echo server using vsock stream.\n");
	fprintf(stderr, "\n");
	fprintf(stderr, "Options:\n");
	fprintf(stderr, "\t-p\tbusy poll on the socket\n");
	fprintf(stderr, "\t-q\tuse seqpacket instead of stream\n");
}

int main(int argc, char **argv)
{
	/* [*] SOCKMAP requires more than 16MiB of locked mem */
	struct rlimit rlim = {
		.rlim_cur = 128 * 1024 * 1024,
		.rlim_max = 128 * 1024 * 1024,
	};

	int busy_poll = 0;
	int sotype = SOCK_STREAM;
	int optc = 0;
	int opt;

	while ((opt = getopt(argc, argv, "pq")) != -1) {
		switch (opt) {
		case 'q':
			sotype = SOCK_SEQPACKET;
			break;
		case 'p':
			busy_poll = 1;
			break;
		default:
			usage(argv[0]);
			exit(1);
			break;
		}
		optc++;
	}

	/* ignore error */
	setrlimit(RLIMIT_MEMLOCK, &rlim);

	/* [*] Prepare ebpf */
	int sock_map = tbpf_create_map(BPF_MAP_TYPE_SOCKMAP, sizeof(int),
				       sizeof(int), 2, 0);
	if (sock_map < 0) {
		PFATAL("bpf(BPF_MAP_CREATE, BPF_MAP_TYPE_SOCKMAP)");
	}

	/* sockmap is only used in prog_verdict */
	tbpf_fill_symbol(bpf_insn_prog_verdict, bpf_reloc_prog_verdict,
			 "sock_map", sock_map);

	/* Load  prog_verdict */
	char log_buf[16 * 1024];
	int bpf_verdict = tbpf_load_program(
		BPF_PROG_TYPE_SK_SKB, bpf_insn_prog_verdict,
		bpf_insn_prog_verdict_cnt, "Dual BSD/GPL",
		KERNEL_VERSION(4, 4, 0), log_buf, sizeof(log_buf));
	if (bpf_verdict < 0) {
		PFATAL("Bpf Log:\n%s\n bpf(BPF_PROG_LOAD, prog_verdict)",
		       log_buf);
	}

	/* Attach maps to programs. */
	int r = tbpf_prog_attach(bpf_verdict, sock_map, BPF_SK_SKB_VERDICT,
			     0);
	if (r < 0) {
		PFATAL("bpf(PROG_ATTACH)");
	}

	if (argc - optc < 2) {
		usage(argv[0]);
		exit(1);
	}

	//add unix server and vsock client to sockmap. vsock client should be argv1
	struct sockaddr_storage connect;
	vsock_parse_sockaddr(&connect, argv[optind]);

	fprintf(stderr, "[+] connecting to %s busy_poll=%d\n", net_ntop(&connect),
		busy_poll);

	int sd = net_bind_unix_dgram();
	if (sd < 0) {
		PFATAL("bind()");
	}
       
	int cd = net_connect_vsock_connectible(&connect, sotype);
	if (cd < 0) {
		PFATAL("connect()");
	}

	//struct sockaddr_storage client;
	//int fd = net_accept(sd, &client);

	/* [*] Perform ebpf socket magic */
	/* Add socket to SOCKMAP. Otherwise the ebpf won't work. */
	int idx = 0;
	int val = cd;
	r = tbpf_map_update_elem(sock_map, &idx, &val, BPF_ANY);
	if (r != 0) {
		if (errno == EOPNOTSUPP) {
			perror("pushing closed socket to sockmap?");
			close(cd);
			return 1;
		}
		PFATAL("bpf(MAP_UPDATE_ELEM)");
	}

	idx = 1;
	val = sd;
	r = tbpf_map_update_elem(sock_map, &idx, &val, BPF_ANY);
	if (r != 0) {
		PFATAL("bpf(MAP_UPDATE_ELEM)");
	}

	/* [*] Wait for the socket to close. Let sockmap do the magic. */
	struct pollfd fds[1] = {
		{.fd = sd, .events = POLLRDHUP},
	};
	poll(fds, 1, -1);

	/* Was there a socket error? */
	{
		int err;
		socklen_t err_len = sizeof(err);
		int r = getsockopt(sd, SOL_SOCKET, SO_ERROR, &err, &err_len);
		if (r < 0) {
			PFATAL("getsockopt()");
		}
		errno = err;
		if (errno) {
			perror("sockmap fd");
		}
	}

	/* Cleanup the entry from sockmap. */
	idx = 0;
	r = tbpf_map_delete_elem(sock_map, &idx);
	if (r != 0) {
		if (errno == EINVAL) {
			fprintf(stderr,
				"[-] Removing closed sock from sockmap\n");
		} else {
			PFATAL("bpf(MAP_DELETE_ELEM, sock_map)");
		}
	}

	idx = 1;
	r = tbpf_map_delete_elem(sock_map, &idx);
	if (r != 0) {
		if (errno == EINVAL) {
			fprintf(stderr,
				"[-] Removing closed sock from sockmap\n");
		} else {
			PFATAL("bpf(MAP_DELETE_ELEM, sock_map)");
		}
	}

	close(sd);
	close(cd);

	return 0;
}
