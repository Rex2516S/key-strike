Usage

The transparent overlay will appear in the top-most layer

Press keys or click mouse buttons to see visual feedback

Mouse CPS (clicks-per-second) is calculated and displayed in real-time

Press F9 at any time to exit the application

Interface Layout
The display is organized in five rows:

Row 1: W key

Row 2: A, S, D keys

Row 3: Shift and C keys

Row 4: Space key

Row 5: LEFT and RIGHT mouse buttons with CPS counters

Controls
W, A, S, D: Movement keys

C: Crouch/sneak key

Shift: Sprint key

Space: Jump key

Mouse Left/Right: Attack/use keys with CPS tracking

F9: Exit application

Technical Details
The application uses a transparent overlay that stays on top of other windows

Keyboard input is captured globally using the keyboard library

Mouse clicks are tracked using the pynput library

CPS is calculated based on clicks within a 1-second rolling window

The interface is built with Tkinter with custom transparent background

Troubleshooting
Common Issues
"Unknown color name" error:

The transparent background feature may not work on all systems

The application will still function with a solid background

Permission errors:

On first run, Windows may ask for permission to monitor keyboard input

Grant permissions for the application to function properly

Application not capturing input:

Ensure no other applications are blocking global keyboard hooks

Run as administrator if necessary

Performance
The application is designed to be lightweight

Typically uses less than 1% CPU and 50MB RAM

If experiencing performance issues, try closing other background applications

Customization
Advanced users can modify the source code to:

Change key bindings

Adjust the visual style

Modify the overlay position and size

Add additional keys or features



i will make a website for this later :D
