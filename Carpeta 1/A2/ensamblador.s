	.file	"Egipcio.c"
	.text
	.section	.rodata
.LC0:
	.string	"%i\n"
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	$100000, -24(%rbp)
	movl	$555, -20(%rbp)
	movl	-24(%rbp), %eax
	cmpl	-20(%rbp), %eax
	jle	.L2
	movl	-20(%rbp), %eax
	movl	%eax, -4(%rbp)
	movl	-24(%rbp), %eax
	movl	%eax, -20(%rbp)
	movl	-4(%rbp), %eax
	movl	%eax, -24(%rbp)
.L2:
	movl	$0, -16(%rbp)
	movl	$1, -12(%rbp)
	movl	$0, -8(%rbp)
	jmp	.L3
.L5:
	movl	-20(%rbp), %eax
	andl	$1, %eax
	testl	%eax, %eax
	je	.L4
	movl	-12(%rbp), %eax
	imull	-24(%rbp), %eax
	addl	%eax, -16(%rbp)
.L4:
	sall	-12(%rbp)
	sarl	-20(%rbp)
	addl	$1, -8(%rbp)
.L3:
	movl	-8(%rbp), %eax
	cmpl	$31, %eax
	jbe	.L5
	movl	-16(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC0(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	$0, %eax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.ident	"GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0"
	.section	.note.GNU-stack,"",@progbits
