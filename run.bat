::blender --background --python wall.py
FOR /R %%G IN (*.blend) DO (blender %%G --background --python wall.py)
