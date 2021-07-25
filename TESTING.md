# Testing

## Bugs Found

1. **Profile Element Being Pushed To Left On Large Screens** - *Fix:* Testing showed that the *navbar-expand-lg* bootstrap class was changing the navbar elements to flex on large screens which messed up the profile position. Removing the class fixed the issue.
2. **DataTables Not Resizing Correctly** - *Fix:* TBC
3. **Cards Stacking On Top Due To Height Constraint** - *Fix:* Add margin bottom and use calc function to calculate height instead.
