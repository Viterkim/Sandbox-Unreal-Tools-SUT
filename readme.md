# Sandbox Unreal Tools (SUT)

# Workflow / Idea
The idea is to have an easy way to do level design in Blender. First you do a rough greybox (before even thinking about modular assets). You aren't always in the lucky position where a modular kit is conveniant in the first step of level designing, and it's very annoying to do double work building some temporary modular assets and then clicking them together in Unreal (and restrictive).

The idea is that you should have a fast and seamless way to build levels (like good old Hammer / Source Engine stuff), and see fast results.

When you are done greyboxing you can then do the "double work" of actually making modular assets and placing them on top of your rough greybox. This should also make stuff less "boxy" and might show you where you need a few unique assets.


# Requirements
Depends on the following addons:

1. [Texel Density Checker 3 Github](https://github.com/mrven/Blender-Texel-Density-Checker) | https://gumroad.com/l/CEIOR
2. [Send To Unreal Github](https://github.com/EpicGames/BlenderTools) (You need to follow this: https://www.unrealengine.com/en-US/blog/download-our-new-blender-addons)

# Setup
1. Follow the "Send to Unreal" steps (which includes enabling remote execution in unreal & python scripting)
  * I recommend going to options and setting "Mesh Folder(Unreal)" to: /Game/Meshes/Dev (or anything you want)
  * Go to the export settings tab, and select "Use object origin"
2. Create Greybox colleciton defaulting to "SUT" (or change it).
3. Do the greyboxing / level designing you need to do. Everything gets merged into a single mesh (unless you check Split collection result).
4. Tick "Send to Unreal" and press SUT
5. In Unreal drag the Meshes/Dev/SM_SUT into your scene, and click the yellow little arrow in the transform panel, to reset it to 0,0,0 coordinates.
6. Put on some proper dev texture (cube material or w.e)
7. Go into Blender -> Change something -> Press SUT -> Instant Changes


![SUT](assets/addon.png)

# Future Features
1. Landscape Synchronization (Rough) (Landscape in unreal -> synchronize to blender and greybox back and forth)
2. Instance Dupliactes in blender to world position in unreal (Make your scene in blender with a modular kit)
