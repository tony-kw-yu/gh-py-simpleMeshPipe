# Fast Mesh Pipe for Rhino-Grasshoppr Python

Code for projects that do not want to depend on external mesh pipe plugins.

# Usage
Create a script component in Rhino and paste the code in from component.py, add the required inputs and outputs (case-sensitive)<br><br>
Rhino 7: Python Script<br>
Rhino 8: Iron Python 2 <br>
<br>

**Inputs** 

| **Name** 	| **Ghtype Hint** 	|
|---	|---	|
| polylines 	| polyline 	|
| radius 	| float 	|
| numSides | int |

**Outputs**
| **Name** 	 |	
|---|
|mesh		|

<br>
Takes a polyline and pipes it with a polygon of radius with numSides.

