CFLAGS := -static
all:
	clang -g -Wall -Wextra -O2 \
		net.c \
		test-burst.c \
		-o test-burst $(CFLAGS)

	clang -g -Wall -Wextra -O2 \
		net.c \
		echo-naive.c \
		-o echo-naive $(CFLAGS)

	clang -g -Wall -Wextra -O2 \
		net.c \
		echo-iosubmit.c \
		-o echo-iosubmit $(CFLAGS)

	clang -g -Wall -Wextra -O2 \
		net.c \
		echo-splice.c \
		-o echo-splice $(CFLAGS)

	clang -Wall -Wextra -O2 -emit-llvm -c \
		echo-sockmap-kern.c \
		-S -o - \
		| llc -march=bpf -filetype=obj -o - \
		| python3 tbpf-decode-elf.py /dev/stdin \
			prog_parser prog_verdict \
		> echo-sockmap-ebpf.c

	clang -g -Wall -Wextra -O2 \
		tbpf.c \
		net.c \
		echo-sockmap-ebpf.c \
		echo-sockmap.c \
		-l elf \
		-o echo-sockmap $(CFLAGS)

	clang -g -Wall -Wextra -O2 \
		tbpf.c \
		net.c \
		echo-sockmap-ebpf.c \
		echo-sockudp.c \
		-l elf \
		-o echo-sockudp $(CFLAGS)

	clang -g -Wall -Wextra -O2 \
		tbpf.c \
		net.c \
		echo-sockmap-ebpf.c \
		echo-vsock.c \
		-l elf \
		-o echo-vsock $(CFLAGS)


.PHONY: format
format:
	clang-format -i *.c *.h
	@grep -n "TODO" *.[ch] || true
