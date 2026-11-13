50% OFFSIDE PROTOTYPE
====================
This is an educational starting point for Trevor's project, not a finished VAR system or an official refereeing tool. The project should be developed and explained by the student, with AI assistance acknowledged where required by the university.

HOW TO RUN
1. Extract the ZIP into a folder on your laptop.
2. Open that folder in VS Code.
3. Open VS Code's terminal and run: python main.py
   If needed on Windows, try: py main.py
4. Choose 1 for a sample or 2 to enter your own measurements.
5. Run tests with: python -m unittest -v

HOW THE MODEL WORKS
- Imagine a straight line running left to right along the pitch. Positions are in the same units, e.g. metres. The program assumes increasing numbers run left to right. The default example uses halfway at 50.
- Measure the attacking player's eligible body as a straight segment on that line. Enter its centre and total length along the direction of attack, excluding hands and arms. A 1D line segment is only an approximation, not a measurement of 50% of a person's actual 3D body.
- Enter the goal-nearest eligible point of each opponent, including the goalkeeper. At least two are needed. The program finds the second-last opponent.
- Enter the ball's goal-nearest point, halfway, and direction of attack. Use the positions at the instant a teammate plays the ball (first contact, except a goalkeeper's throw uses last contact).
- Exactly 50% or more of the attacker's segment beyond the defender qualifies for the custom position test, as in the original code. Change the comparison in analyse_position if the project adopts strictly more than 50%.
- A goal-nearest eligible body part must also be beyond the ball and in the opponents' half. Equality with either is not beyond it. This differs from the original code's centre-based ball and halfway checks.
- Offside position alone is not an offence. You must manually enter whether the player was involved. An immediate direct receipt from a goal kick, throw-in or corner kick is exempt.

IMPORTANT LIMITATIONS
This does not detect players or the ball from video. You enter positions and involvement manually. Camera calibration, tracking, body-part segmentation, accurate timing, multiple cameras, occlusion, uncertainty and referee review are not implemented. A single snapshot cannot model every later match event, including deliberate play or saves. This cannot be used for real match decisions.

The custom 50% rule differs from IFAB Law 11 (including Premier League matches): the official law considers any eligible body part and a player level with the second-last opponent is onside. Exactly 50% ahead corresponds to the segment's centre level with the defender line, and this prototype treats that as meeting the custom threshold. Any actual adoption would require authorization by the relevant governing bodies. Source: https://www.theifab.com/laws/latest/offside/

FILES
- offside.py: the calculation and simple offence checks.
- main.py: interactive console demo.
- test_offside.py: automated edge-case tests.
The old unrelated turtle drawing is intentionally not included; keep your original files as a backup.
