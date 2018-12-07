	.text
	.file	"<string>"
	.globl	main                    # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %entry
	pushq	%rax
	.cfi_def_cfa_offset 16
	movq	$2, a(%rip)
	movl	$fstr, %edi
	xorl	%esi, %esi
	xorl	%eax, %eax
	callq	printf
	xorl	%eax, %eax
	popq	%rcx
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main
	.cfi_endproc
                                        # -- End function
	.type	fstr,@object            # @fstr
	.section	.rodata,"a",@progbits
fstr:
	.asciz	"%f \n"
	.size	fstr, 5


	.section	".note.GNU-stack","",@progbits
