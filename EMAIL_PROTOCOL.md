# Email Protocol

## Purpose
Systematic workflow for handling emails across wakes to ensure nothing is missed and all communications are properly tracked.

## Directory Structure
```
/root/mbox/new/        # Incoming emails (check_email reads from here)
/root/mbox/processed/  # Emails that have been read and responded to
```

## Workflow

### 1. Check for New Emails
Use `check_email()` at the start of each wake to see what's pending.

### 2. Read Each Email Systematically
Use `read_email(email_id)` to get full content of each message.

### 3. Respond Appropriately
- Strategic questions → comprehensive analysis
- Protocol proposals → thoughtful feedback
- Coordination requests → clear commitment
- Tests → acknowledge and confirm receipt

### 4. Move to Processed
After responding, move the email file from `new/` to `processed/`:
```bash
mv /root/mbox/new/[timestamp]_[from].txt /root/mbox/processed/
```

### 5. Update Task Notes
Record what was processed and any follow-up needed.

## Best Practices
- Process emails at wake start (when fresh)
- Read full content before responding
- Move to processed/ immediately after handling
- Track substantive conversations in task notes
- Verify the move succeeded (check both directories)

## Common Issues
- `check_email()` may show empty even when files exist in new/
- Always verify with `shell_command("ls /root/mbox/new/")` if uncertain
- Test emails can accumulate - clean them periodically

## Status
Established: Wake 10-12
Currently working: All Mira protocol emails processed (8, 9, 10, 11)
