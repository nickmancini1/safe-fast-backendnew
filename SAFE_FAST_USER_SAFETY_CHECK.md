# SAFE-FAST User Safety Check

Purpose:
Nick should not need to know code risk.

Before every command, the chat must label the command in simple English:
- read-only
- this can change files
- vendor/paid
- dangerous/destructive

Every command must say:
- what can change
- what cannot change
- what proof should come back
- what counts as done
- what makes the command stop

If the chat cannot explain those things, it must not give the command.

Nick should paste back only the required small block.

## Tightening addendum

Nick does not need to judge the code.
Nick only needs to judge whether the action is sealed.

A safe command must plainly say:
- what can change
- what cannot change
- what proof should come back
- what stops the command
- what means done

If any of that is missing, Nick should not run the command.
