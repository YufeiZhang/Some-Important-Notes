#-------------------------------------------------------------------------------
# Assignment:           4
# Due Date:             March 17, 2014
# Name:                 Yufei Zhang
# Unix ID:              yufei2
# Lecture Section:      B1
# Instructor:           Smith,Jacqueline
# Lab Section:          H03 (Thursday 1400 - 1700)
# Teaching Assistant:   Wanxin Gao
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# in this lab, I found some piece of code on the web and then I wrote the main function to let the stopwatch work. 
#  you need to press "s" to start the stopwatch
#  you can use "s" to start or pause it; "r" to reset it, and "q" to quit the program
#  other things are exactely the same as what is read in eclass

# spim -notrap -mapped_io load "lab4.s"
# using the upper code to run it in the terminal
#-------------------------------------------------------------------------------


.kdata
    __start_msg_:   .asciiz "  Exception "
    __end_msg_:     .asciiz " occurred and ignored\n"
    
    # Messages for each of the 5-bit exception codes
    __exc0_msg:     .asciiz "  [Interrupt] "
    __exc1_msg:     .asciiz "  [TLB]"
    __exc2_msg:     .asciiz "  [TLB]"
    __exc3_msg:     .asciiz "  [TLB]"
    __exc4_msg:     .asciiz "  [Address error in inst/data fetch] "
    __exc5_msg:     .asciiz "  [Address error in store] "
    __exc6_msg:     .asciiz "  [Bad instruction address] "
    __exc7_msg:     .asciiz "  [Bad data address] "
    __exc8_msg:     .asciiz "  [Error in syscall] "
    __exc9_msg:     .asciiz "  [Breakpoint] "
    __exc10_msg:    .asciiz "  [Reserved instruction] "
    __exc11_msg:    .asciiz ""
    __exc12_msg:    .asciiz "  [Arithmetic overflow] "
    __exc13_msg:    .asciiz "  [Trap] "
    __exc14_msg:    .asciiz ""
    __exc15_msg:    .asciiz "  [Floating point] "
    __exc16_msg:    .asciiz ""
    __exc17_msg:    .asciiz ""
    __exc18_msg:    .asciiz "  [Coproc 2]"
    __exc19_msg:    .asciiz ""
    __exc20_msg:    .asciiz ""
    __exc21_msg:    .asciiz ""
    __exc22_msg:    .asciiz "  [MDMX]"
    __exc23_msg:    .asciiz "  [Watch]"
    __exc24_msg:    .asciiz "  [Machine check]"
    __exc25_msg:    .asciiz ""
    __exc26_msg:    .asciiz ""
    __exc27_msg:    .asciiz ""
    __exc28_msg:    .asciiz ""
    __exc29_msg:    .asciiz ""
    __exc30_msg:    .asciiz "  [Cache]"
    __exc31_msg:    .asciiz ""
    __level_msg:    .asciiz "Interrupt mask: "

    #########################################################################
    # Lookup table of exception messages
    __exc_msg_table:
        .word   __exc0_msg, __exc1_msg, __exc2_msg, __exc3_msg, __exc4_msg
        .word   __exc5_msg, __exc6_msg, __exc7_msg, __exc8_msg, __exc9_msg
        .word   __exc10_msg, __exc11_msg, __exc12_msg, __exc13_msg, __exc14_msg
        .word   __exc15_msg, __exc16_msg, __exc17_msg, __exc18_msg, __exc19_msg
        .word   __exc20_msg, __exc21_msg, __exc22_msg, __exc23_msg, __exc24_msg
        .word   __exc25_msg, __exc26_msg, __exc27_msg, __exc28_msg, __exc29_msg
        .word   __exc30_msg, __exc31_msg
    
    # Variables for save/restore of registers used in the handler
    save_v0:    .word   0
    save_a0:    .word   0
    save_a1:    .word   0
    save_at:    .word   0

    #########################################################################
    # This is the exception handler code that the processor runs when
    # an exception occurs. It only prints some information about the
    # exception, but can serve as a model of how to write a handler.
    #
    # Because this code is part of the kernel, it can use $k0 and $k1 without
    # saving and restoring their values.  By convention, they are treated
    # as temporary registers for kernel use.
    #
    # On the MIPS-1 (R2000), the exception handler must be at 0x80000080
    # This address is loaded into the program counter whenever an exception
    # occurs.  For the MIPS32, the address is 0x80000180.
    # Select the appropriate one for the mode in which SPIM is compiled.
    
.ktext  0x80000180
    
        # Save ALL registers modified in this handler, except $k0 and $k1
        # This includes $t* since the user code does not explicitly
        # call this handler.  $sp cannot be trusted, so saving them to
        # the stack is not an option.  This routine is not reentrant (can't
        # be called again while it is running), so we can save registers
        # to static variables.
        sw      $v0, save_v0
        sw      $a0, save_a0
        sw      $a1, save_a1
    
        # $at is the temporary register reserved for the assembler.
        # It may be modified by pseudo-instructions in this handler.
        # Since an interrupt could have occurred during a pseudo
        # instruction in user code, $at must be restored to ensure
        # that that pseudo instruction completes correctly.
        .set    noat
        sw      $at, save_at
        .set    at
    
        # Determine cause of the exception
        mfc0    $k0, $13        # Get cause register from coprocessor 0
        srl     $a0, $k0, 2     # Extract exception code field (bits 2-6)
        andi    $a0, $a0, 0x1f
        
        # Check for program counter issues (exception 6)
        bne     $a0, 6, ok_pc
        nop
    
        mfc0    $a0, $14        	 # EPC holds PC at moment exception occurred
        andi    $a0, $a0, 0x3   	 # Is EPC word-aligned (multiple of 4)?
        beqz    $a0, ok_pc
        nop
    
        # Bail out if PC is unaligned
        # It's not really kosher doing syscalls in an exception handler,
        # but this handler is just for demonstration and this keeps it short
        li      $v0, 4
        la      $a0, __exc3_msg
        syscall
        li      $v0, 10
        syscall
    
ok_pc:
        mfc0    $k0, $13
        srl     $a0, $k0, 2     	 # Extract exception code from $k0 again
        andi    $a0, $a0, 0x1f
        bnez    $a0, non_interrupt # Code 0 means exception was an interrupt
        nop
    
        # External interrupt handler
        # Don't skip instruction at EPC since it has not executed.
        # Interrupts occur BEFORE the instruction at PC executes.
        # Other exceptions occur during the execution of the instruction,
        # hence for those e increment the return address to avoid
        # re-executing the instruction that caused the exception.
    
        # Print interrupt level
        # It's not really kosher doing syscalls in an exception handler,
        # but this handler is just for demonstration and this keeps it short
        
# ------------- up to this line, all of the codes are copy form ------------- #
# --- http://www.cs.uwm.edu/classes/cs315/Bacon/Lecture/HTML/ch15s10.html --- #

        # BIND keyboard and timer interrupt written by me
        
        srl     $a0 $k0 11         # check keyboard interrupt
        andi    $a0 $a0 1
        bnez    $a0 kbd_interrput

        srl     $a0 $k0 15         # check timer interrupt
        andi    $a0 $a0 1
        bnez    $a0 timer_interrput

        j       return

# -------------------------- countinue copying form -------------------------- #
# --- http://www.cs.uwm.edu/classes/cs315/Bacon/Lecture/HTML/ch15s10.html --- #

non_interrupt:
        # Print information about exception.
        # It's not really kosher doing syscalls in an exception handler,
        # but this handler is just for demonstration and this keeps it short
        li      $v0, 4          	 # print_str
        la      $a0, __start_msg_
        syscall
    
        li      $v0, 1          	 # print_int
        mfc0    $k0, $13        	 # Extract exception code again
        srl     $a0, $k0, 2
        andi    $a0, $a0, 0x1f
        syscall
    
        # Print message corresponding to exception code
        # Exception code is already shifted 2 bits from the far right
        # of the cause register, so it conveniently extracts out as
        # a multiple of 4, which is perfect for an array of 4-byte
        # string addresses.
        # It's not really kosher doing syscalls in an exception handler,
        # but this handler is just for demonstration and this keeps it short
        li      $v0, 4             # print_str
        mfc0    $k0, $13        	 # Extract exception code without shifting
        andi    $a0, $k0, 0x7c
        lw      $a0, __exc_msg_table($a0)
        nop
        syscall
    
        li      $v0, 4          	 # print_str
        la      $a0, __end_msg_
        syscall
    
        # Return from (non-interrupt) exception. Skip offending instruction
        # at EPC to avoid infinite loop.
        mfc0    $k0, $14
        addiu   $k0, $k0, 4
        mtc0    $k0, $14
    
return:
        # Restore registers and reset processor state
        # ----------------------------------------------------------------------
        lw      $v0, save_v0    	 # Restore other registers
        lw      $a0, save_a0
        lw      $a1, save_a1

        .set    noat            	 # Prevent assembler from modifying $at
        lw      $at, save_at
        .set    at
    
        mtc0    $zero, $13      	 # Clear Cause register
    
        # Re-enable interrupts, which were automatically disabled
        # when the exception occurred, using read-modify-write cycle.
        mfc0    $k0, $12        	 # Read status register
        andi    $k0, 0xfffd        # Clear exception level bit
        ori     $k0, 0x0001        # Set interrupt enable bit
        mtc0    $k0, $12           # Write back
    
        # Return from exception on MIPS32:
        eret
    
# ------------------------------- End Copying -------------------------------- #

# ------------------------------ Begin Writing ------------------------------- #

# The interrupt cause by keyboard.
kbd_interrput:
        lw      $a1 0xffff0000
        andi    $a1 $a1, 0x1       # set 1 to enable next map io
        beqz    $a1 kbd_interrput  # wait for hardware set bit 0
        lw      $a1 0xffff0004     # read ascii of keyboard input

        xori    $a0 $a1 0x71       # check for 'q'
        beqz    $a0 quit
        xori    $a0 $a1 0x72       # check for 'r'
        beqz    $a0 reset
        xori    $a0 $a1 0x73       # check for 's'
        beqz    $a0 pause
        j       kbd_reenable

kbd_reenable:                      # reenable kbd_interrput
        li      $a0 2
        sw      $a0 0xffff0000
        j       return

timer_interrput:                   # the interrupt caused by timer
        beq     $s5 0 timer_reset  # 0 -> press start to start
        addi    $s3 $s3 1          # increase the seconds
        xori    $a0 $s3 0x0a       # if second == 10, call increase ?0
        beqz    $a0 inc_second
        j       timer_reset
 
inc_second:                        # increase second decade
        li      $s3 0
        addi    $s2 $s2 1          # increase the seconds
        xori    $a0 $s2 0x06       # if x = 60
        beqz    $a0 inc_minute
        j       timer_reset

inc_minute:                        # incesaer minutes
        li      $s2 0              # set 0 to the ten of second
        addi    $s1 $s1 1
        xori    $a0 $s1 0x0a       # if minute == 10, call increase ?0
        beqz    $a0 inc_minute2
        j       timer_reset

inc_minute2:                       # increase minutes
        li      $s1 0
        addi    $s0 $s0 1
        xori    $a0 $s0 0x06       # if x = 60
        beqz    $a0 reset          # if 60:00 then reset it to be 00:00
        j       timer_reset

reset:                             # reset the timer to 00:00
        li      $s0 0              # reset minutes
        li      $s1 0              # reset minutes
        li      $s2 0              # reset seconds
        li      $s3 0              # reset seconds
        li      $s4 1              # ready to print time
        j       kbd_reenable       # print current time

timer_reset:                       # set $11 and wait for next seconds
        mtc0    $zero $9
        li      $s4 1              # ready to print time
        j       return

quit:                              # exit the program
        li      $v0 10
        syscall

pause:
        xori    $s5 $s5 0x1
        j       return

.text
        .globl __start
__start:
        lw      $a0 0($sp)         # argc = *$sp
        addiu   $a1 $sp 4          # argv = $sp + 4
        addiu   $a2 $sp 8          # envp = $sp + 8
        sll     $v0 $a0 2          # envp += size of argv array
        addu    $a2 $a2 $v0
        jal     main
        nop
        li      $v0, 10            # exit
        syscall
    
        .globl __eoth
__eoth:

# ------------------------ main function starts here ------------------------- #
#s0 -> the minuts for ?0
#s1 -> the minuts for 0?
#s2 -> the second for ?0
#s3 -> the second for 0?
#s4 -> prepare for printing

.data 
time:           .asciiz "00:00"
buffer:         .byte 0x08 0x08 0x08 0x08 0x08
                .asciiz "88:88"    # buffer -> \r\r\r\r\r88:88
int2str:        .asciiz "0123456789"

.text
main:
        li      $s0 0              # initialized the timmer
        li      $s1 0
        li      $s2 0
        li      $s3 0
        li      $s4 0
        li      $t0 0              # print initial time which is 00:00
        j       print_initime

ini_interrput:
        mtc0    $zero $9
        addi    $t0 $zero 100
        mtc0    $t0 $11
        li      $t0 0
        ori     $t0 0x8801         # set bits 11 and 15 and enable interrupt
        mtc0    $t0 $12
        li      $t0 2
        sw      $t0 0xffff0000
        j       loop

print_initime:
        xori    $t1 $t0 5
        beqz    $t1 ini_interrput
        lb      $a0 time($t0)
        j       putchat_ini

print_ininext:
        addi    $t0 $t0 1
        j       print_initime

putchat_ini:
        lw      $v0 0xffff0008
        andi    $v0 $v0 0x0001
        beqz    $v0 putchat_ini    # bit 0  == 0 -> not ready
        sw      $a0 0xffff000c
        j       print_ininext

loop:
        beqz    $s4 loop           # wait for interrupt
        li      $t0 5
        lb      $t2 int2str($s0)   # load time ?0:00
        sb      $t2 buffer ($t0)
        addi    $t0 $t0 1          # load time 0?:00
        lb      $t2 int2str($s1)
        sb      $t2 buffer ($t0)
        addi    $t0 $t0 2          # load time 00:?0
        lb      $t2 int2str($s2)
        sb      $t2 buffer ($t0)
        addi    $t0 $t0 1          # load time 00:0?
        lb      $t2 int2str($s3)
        sb      $t2 buffer ($t0)
        li      $t0 0              # reset position and status
        li      $s4 0
        j       LoP                # goto Loop of Printing

LoP:
        xori    $t1 $t0 10
        beqz    $t1 loop
        lb      $a0 buffer($t0)
        j       putchat_time

LoP2:
        addi    $t0 $t0 1
        j       LoP

putchat_time:
        lw      $v0 0xffff0008
        andi    $v0 $v0 0x0001
        beqz    $v0 putchat_time   # bit 0  == 0 -> not ready
        sw      $a0 0xffff000c
        j       LoP2

