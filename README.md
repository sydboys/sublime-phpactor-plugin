# sublime-phpactor-plugin

Available commands in the command palette (CTRL+P):
```
[
  { "caption": "Phpactor: Status", "command": "phpactor_echo", "args": { "message": "Phpactor Status: OK" } },
  { "caption": "Phpactor: Offset Info", "command": "phpactor_offset_info" },
  { "caption": "Phpactor: Context Menu", "command": "phpactor_context_menu" },
  { "caption": "Phpactor: Navigate", "command": "phpactor_navigate" },
  { "caption": "Phpactor: Goto Definition", "command": "phpactor_goto_definition" },
  { "caption": "Phpactor: Goto Type", "command": "phpactor_goto_type" },
  { "caption": "Phpactor: Goto Implementation", "command": "phpactor_goto_implementation" },
  { "caption": "Phpactor: Find References", "command": "phpactor_references" },
  { "caption": "Phpactor: Transform", "command": "phpactor_transform" },
  { "caption": "Phpactor: Transform - Complete Constructor", "command": "phpactor_transform", "args": { "transform": "complete_constructor" } },
  { "caption": "Phpactor: Transform - Add Missing Properties", "command": "phpactor_transform", "args": { "transform": "add_missing_properties" } },
  { "caption": "Phpactor: Transform - Fix Namespace & Class Name", "command": "phpactor_transform", "args": { "transform": "fix_namespace_class_name" } },
  { "caption": "Phpactor: Transform - Implement Contracts", "command": "phpactor_transform", "args": { "transform": "implement_contracts" } },
  { "caption": "Phpactor: Generate Accessor", "command": "phpactor_generate_accessor" },
  { "caption": "Phpactor: Generate Method", "command": "phpactor_generate_method" },
  { "caption": "Phpactor: Extract Constant", "command": "phpactor_extract_constant" },
  { "caption": "Phpactor: Extract Expression", "command": "phpactor_extract_expression" },
  { "caption": "Phpactor: Extract Method", "command": "phpactor_extract_method" },
  { "caption": "Phpactor: Override Method", "command": "phpactor_override_method" },
  { "caption": "Phpactor: Change Visibility", "command": "phpactor_change_visibility" },
  { "caption": "Phpactor: Rename Variable", "command": "phpactor_rename_variable" },
  { "caption": "Phpactor: Import Class", "command": "phpactor_import_class" },
  { "caption": "Phpactor: Import Missing Classes", "command": "phpactor_import_missing_classes" },
  { "caption": "Phpactor: Copy Class", "command": "phpactor_copy_class" },
  { "caption": "Phpactor: Move Class", "command": "phpactor_move_class" },
  { "caption": "Phpactor: Class New", "command": "phpactor_class_new" },
  { "caption": "Phpactor: Class Inflect", "command": "phpactor_class_inflect" },
]
```

You can bind any of these commands to key-combination in the sublime-keymap config (Preferences > Key Bindings).
For example to show the phpactor's context menu on "alt+enter":
```
{ "keys": ["alt+enter"], "command": "phpactor_context_menu" }
```
Another example to run phpactor's goto definition on "F12":
```
{ "keys": ["f12"], "command": "phpactor_goto_definition" }
```

You can also bind commands to mouse actions in the sublime-mousemap config (not available in the menu, need to manually create a "Default (Linux).sublime-mousemap" file).
For example to run the phpactor's goto definition command on "ctrl+leftmousebuttonclick":
```
[
    {
        "button": "button1", 
        "count": 1, 
        "modifiers": ["ctrl"],
        "press_command": "drag_select",
        "command": "phpactor_goto_definition"
    }
]
```
