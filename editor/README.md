This directory contains images to replace the the STI files of Editor.slf.

This file describes which images are required, their size and purpose.

The required images depend on what the STI is used for.

All the images in the same STI must share the same palette.

| Usage        | Required Images |
| ------------ | --------------- |
| check box    | 0=off, 1=off+hilite, 2=on, 3=on+hilite |
| radio button | 0=off, 1=off+hilite, 2=on, 3=on+hilite |
| button       | 1=normal, 2=normal+hilite, 3=pressed, 4=pressed+hilite |
| full button  | 0=grayed, 1=normal, 2=normal+hilite, 3=pressed, 4=pressed+hilite |
| dir buttons  | 0=northwest, 1=north, 2=northeast, 3=east, 4=southeast", 5=south, 6=southwest, 7=west |
| image button | 0=image |
| image        | 0=image |
| not used     |  |

For button, image 0 always exists but isn't used so it's not required.

The following list was created from the list of image sizes provided by @selaux and the ja2-stracciatella code in `src/game/editor`:

| File Name            | Size           | Details |
| -------------------- | -------------- | ------- |
| ADDROOM.STI          | 30x30          | not used, has 5 images |
| ADDTILEROOM.STI      | 30x30          | button, "Draw room number" |
| ARROWSOFF.STI        | 29x29 or 30x30 | dir buttons, "Edit merc direction", 0+2+4+6=29x29 and 1+3+5+7=30x30 |
| ARROWSON.STI         | 29x29 or 30x30 | dir buttons? loaded but never used, 0+2+4+6=29x29 and 1+3+5+7=30x30 |
| BANKS.STI            | 30x30          | button, "Place banks and cliffs" |
| BIGX.STI             | 29x29          | image button, cancel |
| CANCEL.STI           | 30x30          | full button, cancel |
| CAVES.STI            | 30x30          | button, "Edit cave walls" |
| CENTER.STI           | 30x21          | button, "Specify center point" |
| CHECKBOX.STI         | 15x15          | check box |
| CHECKMARK.STI        | 31x27          | image button, ok |
| COPYROOM.STI         | 30x30          | button, "Copy a building" |
| CRACKWALL.STI        | 30x30          | button, "Place damaged walls" |
| DEBRIS.STI           | 30x30          | button, "Place debris" |
| DECAL.STI            | 30x30          | button, "Place wall decals" |
| DECOR.STI            | 30x30          | button, "Place furniture" |
| DELROOM.STI          | 30x30          | button, "Remove a building" |
| DOOR.STI             | 30x30          | button, "Place doors" |
| DOWNARROW.STI        | 30x30          | button, down arrow |
| DOWNGRID.STI         | 30x30          | button, "Draw ground textures" |
| EAST.STI             | 30x20          | button, "Specify east point" |
| ERASER.STI           | 30x30          | button, erase |
| EDITMODEBG.STI       | 640x120        | not used, image? |
| EXCLAMATION.STI      | 4x20           | image |
| EXITGRIDBUT.STI      | 30x30          | button, "Add exit grids" |
| EXITGRIDQ.STI        | 30x30          | not used, has 5 images: 0+1+2+3+4=30x30 (button?) |
| EXITGRIDXBUT.STI     | 30x30          | not used, has 5 images: 0+1+2+3+4=30x30 (button?) |
| FAKELIGHT.STI        | 30x30          | button, "Toggle fake ambient lights" |
| FILL.STI             | 30x30          | button, "Fill area" |
| FLOOR.STI            | 30x30          | button, "Place floors" |
| INVPANEL.STI         | 300x99         | image, merc inventory panel |
| ISOLATED.STI         | 30x21          | button, "Specify isolated point" |
| KEY.STI              | 30x30          | button, "Lock or trap existing doors" |
| KEYIMAGE.STI         | 12x22          | image |
| KILLTILEROOM.STI     | 30x30          | button, "Erase room numbers" |
| LEFTARROW.STI        | 30x20          | button, left arrow |
| LEFTSCROLL.STI       | 49x39          | button, scroll left |
| LGDOWNARROW.STI      | 28x41          | image button, scrool down |
| LGUPARROW.STI        | 28x41          | image button, scroll up |
| LIGHT.STI            | 30x30          | button, "Add ambient light source", has 1 extra image: 5=3x2 |
| LIGHT2.STI           | 30x30?         | not used, has 6 images: 0+1+2+3+4=30x30 (button?) and 5=3x2 |
| LOAD.STI             | 30x30          | button, load |
| MERCAPPEARANCE.STI   | 34x26          | button, "Physical appearance mode", has 2 extra images: 5=625x26 and 6=800x572 |
| MERCATTRIBUTES.STI   | 34x26          | button, "Attributes mode", has 2 extra images: 5=625x26 and 6=800x572 |
| MERCGENERAL.STI      | 34x26          | button, "General information mode", has 2 extra images: 5=625x26 and 6=800x572 |
| MERCGLOWSCHEDULE.STI | 34x26          | button, "Schedule mode" |
| MERCINVENTORY.STI    | 34x26          | button, "Inventory mode" |
| MERCPROFILE.STI      | 34x26          | button, "Profile ID mode", has 2 extra images: 5=625x26 and 6=800x572 |
| MERCSCHEDULE.STI     | 34x26          | button, "Schedule mode", has 2 extra images: 5=625x26 and 6=800x572 |
| MOVEROOM.STI         | 30x30          | button, "Move a building" |
| NEW.STI              | 30x30          | button, new |
| NEWROOF.STI          | 30x30          | button, "Add/replace building's roof", has 2 extra images: 5=645x30 and 6=800x568 |
| NEWROOM.STI          | 30x30          | button, "Add a new room" |
| NORTH.STI            | 30x20          | button, "Specify north point" |
| NUM1.STI             | 30x30          | button, "Place rocks", has 1 extra image: 5=3x2 |
| NUM2.STI             | 30x30          | button, "Place barrels & other junk", has 1 extra image: 5=3x2 |
| NUM3.STI             | 30x30          | not used, has 6 images: 0+1+2+3+4=30x30 (button?) and 5=3x2 |
| NUM4.STI             | 30x30          | not used, has 6 images: 0+1+2+3+4=30x30 (button?) and 5=3x2 |
| OK.STI               | 30x30          | full button, ok, has 1 extra image: 5=398x130 |
| OMERTA.STI           | 212x212        | image, map of Arulco (16x16 grid, 2 pixel border) |
| PAINT.STI            | 30x30          | button, "Cycle brush size" |
| RADIOBUTTON.STI      | 12x12          | radio button |
| RIGHTARROW.STI       | 30x20          | button, right arrow |
| RIGHTSCROLL.STI      | 49x39          | button, scroll right |
| ROAD.STI             | 30x30          | button, "Place roads" |
| ROOF.STI             | 30x30          | button, "Place roofs" |
| SAVE.STI             | 30x30          | button, save |
| SAWROOM.STI          | 30x30          | button, "Remove an area from existing building" |
| SMCHECKBOX.STI       | 12x12          | check box |
| SOUTH.STI            | 30x20          | button, "Specify south point" |
| TILESET.STI          | 30x30          | button, "Select tileset" |
| TOILET.STI           | 30x30          | button, "Place generic furniture" |
| TREE.STI             | 30x30          | button, "Place trees & bushes" |
| UNDO.STI             | 30x30          | button, undo |
| UPARROW.STI          | 30x30          | button, up arrow |
| UPGRID.STI           | 30x30          | button, "Set map ground textures" |
| WALL.STI             | 30x30          | button, "Place walls" |
| WEST.STI             | 30x20          | button, "Specify west point" |
| WINDOW.STI           | 30x30          | button, "Place windows" |
