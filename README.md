High-Level objetcives
- Incorporate requirements
- Data persistence (so that data is retained even after program stop)
- Responsive GUI
- Idempotency (clicking multiple times doesn't give duplicate data)
- Ease of use (not all Guest fields required)

Coding architecture
- As much as possible, put every action into a definition
- Main GUI elements global,s o they can be referenced from any function
- decided to use comma-separated value for files to make the data transparent

Gotchas
- Listbox exportselection=False to avoid losing the listbox selection when you click around
- Listbox change event has an input (more), that shows the virtual event, but x and y always equal 0.  Don't understand why.
- Try / Except on change_event, because sometimes the list index came back as 0 or not defined
- Subset of list to get all possible guests [2:]
