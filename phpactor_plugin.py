import sublime
import sublime_plugin
import tksublime
import phpactor
import os

#################################################
# Public Commands [SUBLIME-PHPACTOR] -> Phpactor
#################################################

class PhpactorRpcCommand(sublime_plugin.TextCommand):
    def run(self, edit, action, parameters):
        phpactor = phpactor.Phpactor(self.get_phpactor_settings())
        phpactor.send_rpc_request(self.build_rpc_request(action, parameters), self.before_send, self.on_error, self.on_done)

    def build_rpc_request(self, action, parameters):
        if 'source' in parameters:
            parameters['source'] = parameters['source'].replace('@current_source', self.get_current_file_content())

        if 'path' in parameters:
            parameters['path'] = parameters['path'].replace('@current_path', self.get_current_file_path())

        if 'source_path' in parameters:
            parameters['source_path'] = parameters['source_path'].replace('@current_path', self.get_current_file_path())

        if 'current_path' in parameters:
            parameters['current_path'] = parameters['current_path'].replace('@current_path', self.get_current_file_path())

        if 'offset' in parameters:
            parameters['offset'] = int(str(parameters['offset']).replace('@current_offset', str(self.get_current_position())))

        if 'offset_start' in parameters:
            parameters['offset_start'] = int(str(parameters['offset_start']).replace('@current_offset_start', str(self.get_current_position_start())))

        if 'offset_end' in parameters:
            parameters['offset_end'] = int(str(parameters['offset_end']).replace('@current_offset_end', str(self.get_current_position_end())))

        return Phpactor.Rpc.Request(action, parameters)

    def get_phpactor_settings(self):
        return Phpactor.Settings(
            self.get_phpactor_bin(),
            tksublime.find_working_dir(self.view)
        )

    def get_current_position(self):
        for region in self.view.sel():
            return region.begin()

    def get_current_position_start(self):
        for region in self.view.sel():
            return region.begin()

    def get_current_position_end(self):
        for region in self.view.sel():
            return region.end()

    def get_current_file_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def get_current_file_path(self):
        file_path = self.view.file_name();

        if file_path:
            return file_path

        return "" # unsaved file

    def get_phpactor_bin(self):
        return '/home/tkotosz/Sites/phpactor/bin/phpactor' # TODO get this from settings

    def before_send(self, request):
        tksublime.log_rpc_request(request)

    def on_error(self, err):
        tksublime.log_rpc_error(err.message)
        self.dispatch_rpc_editor_action('error', { 'message': 'RPC request failed with unknown error (see logs)', 'details': err.message })

    def on_done(self, response):
        tksublime.log_rpc_response(response)
        self.dispatch_rpc_editor_action(response.action, response.parameters)

    def dispatch_rpc_editor_action(self, name, parameters):
        self.view.run_command('phpactor_dispatch_rpc_editor_action', { 'name': name, 'parameters': parameters })

class PhpactorDispatchRpcEditorActionCommand(sublime_plugin.TextCommand):
    def run(self, edit, name, parameters):
        tksublime.log_editor_action({'name': name, 'parameters': parameters})
        self.view.run_command('phpactor_editor_action_' + name, parameters)

class PhpactorEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'echo',
            'parameters': {
                'message': 'Phpactor Status: OK'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'goto_definition',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'target': 'focused_window'
            }
        }

        self.view.run_command('phpactor_rpc', request)

class PhpactorGotoTypeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'goto_type',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'target': 'focused_window'
            }
        }

        self.view.run_command('phpactor_rpc', request)

# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "complete_constructor" } },
# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "add_missing_properties" } },
# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "fix_namespace_class_name" } },
# { "keys": ["<key>"], "command": "phpactor_transform", "args": { "transform": "implement_contracts" } },
class PhpactorTransformCommand(sublime_plugin.TextCommand):
    def run(self, edit, transform = None):
        request = {
            'action': 'transform',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'transform': transform
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorImportClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'import_class',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorCopyClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'copy_class',
            'parameters': {
                'source_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorMoveClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'move_class',
            'parameters': {
                'source_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorOffsetInfoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'offset_info',
            'parameters': {
                'source': '@current_source',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorClassNewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'class_new',
            'parameters': {
                'current_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorClassInflectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'class_inflect',
            'parameters': {
                'current_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorReferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'references',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
                #'filesystem': 'composer'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorExtractConstantCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'extract_constant',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorGenerateMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'generate_method',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorGenerateAccessorsCommand(sublime_plugin.TextCommand):
    def run(self, edit, names=None):
        request = {
            'action': 'generate_accessor',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorContextMenuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'context_menu',
            'parameters': {
                'source': '@current_source',
                'current_path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorNavigateCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'navigate',
            'parameters': {
                'source_path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorImportMissingClassesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'import_missing_classes',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorOverrideMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'override_method',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorChangeVisibilityCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'change_visibility',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }

        self.view.run_command('phpactor_rpc', request)

class PhpactorExtractExpressionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'extract_expression',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset_start': '@current_offset_start',
                'offset_end': '@current_offset_end'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorExtractMethodCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'extract_method',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset_start': '@current_offset_start',
                'offset_end': '@current_offset_end'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorRenameVariableCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'rename_variable',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset'
            }
        }
        self.view.run_command('phpactor_rpc', request)

class PhpactorGotoImplementationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'goto_implementation',
            'parameters': {
                'source': '@current_source',
                'path': '@current_path',
                'offset': '@current_offset',
                'target': 'focused_window'
            }
        }
        self.view.run_command('phpactor_rpc', request)

############################################################################
# Internal Helper Commands (Currently Unused) [SUBLIME-PHPACTOR] -> Phpactor
############################################################################

class PhpactorFileInfoCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        request = {
            'action': 'file_info',
            'parameters': {
                'path': '@current_path'
            }
        }

        # TODO - This returns a "return" editor action which should be consumed directly then anything can done with it
        self.view.run_command('phpactor_rpc', request)

class PhpactorClassSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        keyword = self.get_current_word()

        if not keyword:
            return

        request = {
            'action': 'class_search',
            'parameters': {
                'short_name': keyword
            }
        }

        # TODO - This returns a "return_choice" editor action which should be consumed directly then anything can done with it
        self.view.run_command('phpactor_rpc', request)

    def get_current_word(self):
        keyword = ''
        for region in self.view.sel():
            if region.begin() == region.end():
                word = self.view.word(region)
            else:
                word = region

            if not word.empty():
                keyword = self.view.substr(word)
        
        return keyword

##################################################################
# Internal Commands (Editor Actions) [SUBLIME-PHPACTOR] -> Sublime
##################################################################

class PhpactorEditorActionEchoCommand(sublime_plugin.TextCommand):
    def run(self, edit, message = "Hello"):
        sublime.run_command('tk_show_status_message', { 'message': message })

class PhpactorEditorActionErrorCommand(sublime_plugin.TextCommand):
    def run(self, edit, message, details):
        sublime.run_command('tk_show_status_message', { 'message': 'Phpactor Error: ' + message })

class PhpactorEditorActionCollectionCommand(sublime_plugin.TextCommand):
    def run(self, edit, actions):
        for action in actions:
            self.view.run_command('phpactor_dispatch_rpc_editor_action', action)

class PhpactorEditorActionFileReferencesCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_references):
        window = self.view.window();
        original_selections = [r for r in self.view.sel()]

        files = []
        options = []
        for file_reference in file_references:
            for line_reference in file_reference['references']:
                pos = ":" + str(line_reference['line_no']) + ":" + str(line_reference['col_no'] + 1) # col starts from 1 in sublime, api returns from 0
                file_name = os.path.basename(file_reference['file'])
                file_absolute_path = file_reference['file']
                file_relative_path = file_absolute_path.replace(tksublime.find_working_dir(view) + '/', '')
                files.append(file_absolute_path + pos);
                options.append([file_name + pos, file_relative_path + pos])
        
        window.show_quick_panel(
            options,
            on_select=lambda index: self.open_file(index, files, window, self.view, original_selections),
            on_highlight=lambda index: self.show_preview(index, files, window)
        )

    def open_file(self, index, files, window, original_view, original_selections):
        if index == -1:
            # restore original view
            original_view.sel().clear()
            original_view.sel().add_all(original_selections)
            window.focus_view(original_view)
            original_view.show(original_selections[0])
            return

        window.run_command('tk_open_file', { 'file_path': files[index] })

    def show_preview(self, index, files, window):
        window.run_command('tk_open_file_preview', { 'file_path': files[index] })

class PhpactorEditorActionInputCallbackCommand(sublime_plugin.TextCommand):
    def run(self, edit, inputs, callback):    
        input = inputs.pop(0)

        next = None
        if len(inputs) > 0: # we have more inputs
            next = lambda callback: self.view.run_command('phpactor_editor_action_input_callback', { 'inputs': inputs, 'callback': callback })

        if input['type'] == 'list':
            items = []

            if input['parameters']['multi']:
                items.append('All')

            for item in input['parameters']['choices']:
                items.append(item)

            self.view.window().show_quick_panel(
                items,
                on_select=lambda index: self.select_item(index, items, input['name'], input['parameters']['multi'], callback, next)
            )

        if input['type'] == 'choice':
            items = []

            for item in input['parameters']['choices']:
                items.append(item)

            self.view.window().show_quick_panel(
                items,
                on_select=lambda index: self.select_item(index, items, input['name'], False, callback, next)
            )

        if input['type'] == 'text':
            self.view.window().show_input_panel(
                input['parameters']['label'],
                input['parameters']['default'],
                lambda alias: self.handle_input(alias, input['name'], callback, next),
                None,
                None
            )

        if input['type'] == 'confirm':
            message = []
            for line in input['parameters']['label'].split('\n'):
                message.append(line.strip())

            callback['parameters'][input['name']] = sublime.ok_cancel_dialog('\n\n'.join(message), 'Confirm')

            if not next:
                self.view.run_command('phpactor_rpc', callback)
            else:
                next(callback)

    def select_item(self, index, items, property_name, is_multi, callback, next):
        if index == -1:
            return;

        if is_multi:
            if items[index] == 'All':
                del items[index]
                callback['parameters'][property_name] = items
            else:
                callback['parameters'][property_name] = [items[index]]
        else:
            callback['parameters'][property_name] = items[index]

        if not next:
            self.view.run_command('phpactor_rpc', callback)
        else:
            next(callback)

    def handle_input(self, alias, property_name, callback, next):
        callback['parameters'][property_name] = alias

        if not next:
            self.view.run_command('phpactor_rpc', callback)
        else:
            next(callback)

class PhpactorEditorActionUpdateFileSourceCommand(sublime_plugin.TextCommand):
    def run(self, edit, path, edits, source):
        # TODO FIX cursor position after source update
        self.view.run_command('tk_replace_file_content', { 'file_path': path, 'source': source } )

class PhpactorEditorActionOpenFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, force_reload, path, offset, target):
        # navigate command returns relative path for some reason
        if path.find('/') != 0:
            path = tksublime.find_working_dir(view) + '/' + path

        self.view.window().run_command('tk_open_file_at_offset', { 'file_path': path, 'offset': offset } )

class PhpactorEditorActionCloseFileCommand(sublime_plugin.TextCommand):
    def run(self, edit, path):
        self.view.window().run_command('tk_close_file', { 'file_path': path } )

class PhpactorEditorActionInformationCommand(sublime_plugin.TextCommand):
    def run(self, edit, information):
        debug_view = self.view.window().create_output_panel('phpactor_information')
        debug_view.set_syntax_file('Packages/JavaScript/JSON.sublime-syntax')
        debug_view.insert(edit, 0, information)
        self.view.window().run_command('show_panel', { 'panel': 'output.phpactor_information' })


###########################
# Reusable Sublime Commands
###########################

class TkShowStatusMessageCommand(sublime_plugin.ApplicationCommand):
    def run(self, message):
        sublime.status_message(message)

class TkOpenFileCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        self.window.open_file(file_path, sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.window.active_group())

class TkCloseFileCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        file_view = self.window.find_open_file(file_path)
        file_view.close() # undocumented function but exists! (otherwise I would have to switch to it, trigger a close current file then switch back)

class TkOpenFilePreviewCommand(sublime_plugin.WindowCommand):
    def run(self, file_path):
        self.window.open_file(file_path, sublime.TRANSIENT | sublime.ENCODED_POSITION | sublime.FORCE_GROUP, self.window.active_group())

class TkOpenFileAtOffsetCommand(sublime_plugin.WindowCommand):
    def run(self, file_path, offset):
        self.window.run_command('tk_open_file', { 'file_path': file_path })
        self.window.run_command('tk_jump_to_offset', { 'offset': offset })

class TkJumpToOffsetCommand(sublime_plugin.WindowCommand):
    view = None
    offset = 0
    def run(self, offset):
        view = self.window.active_view();
        if view.is_loading(): # need to wait for file open (see TkJumpToOffsetFileOpenedEventListener)
            TkJumpToOffsetCommand.view = view
            TkJumpToOffsetCommand.offset = int(offset)
            return;

        view.sel().clear()
        view.sel().add(sublime.Region(offset))
        sublime.set_timeout(lambda: view.show_at_center(offset), 0)

class TkJumpToOffsetFileOpenedEventListener(sublime_plugin.EventListener):
    # very weird but only "on_load_async" + "set_timeout" combination works reliably for some reason :/
    def on_load_async(self,view):
        if view == TkJumpToOffsetCommand.view:
            offset = TkJumpToOffsetCommand.offset
            view.sel().clear()
            view.sel().add(sublime.Region(offset))
            sublime.set_timeout(lambda: view.show_at_center(offset), 0)
            TkJumpToOffsetCommand.file_path = ''
            TkJumpToOffsetCommand.offset = ''

class TkReplaceFileContentCommand(sublime_plugin.TextCommand):
    def run(self, edit, file_path, source):
        self.view.window().run_command('tk_open_file', { 'file_path': file_path })
        file_view = self.view.window().find_open_file(file_path)
        if file_view: # something went wrong while opening the file
            file_view.replace(edit, sublime.Region(0, file_view.size()), source)