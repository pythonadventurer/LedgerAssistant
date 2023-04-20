"""
# Credit

- Created by Mitja Martini on 2008-11-29.
- Updated by Russell Adams, 2011/01/24 to support Python 3 and Combobox.
   Licensed same as original (not specified?), or public domain, whichever is less restrictive.
- AutocompleteCombobox Modified by Rob Fowler, 2023-04-18.

See:
https://mail.python.org/pipermail/tkinter-discuss/2012-January/003041.html

"""
import tkinter
import tkinter.ttk

class AutocompleteCombobox(tkinter.ttk.Combobox):

        def __init__(self,parent):
            tkinter.ttk.Combobox.__init__ (self,parent)

        def autocomplete(self, delta=0):
                """autocomplete the Combobox, delta may be 0/1/-1 to cycle through possible hits"""
                if delta: # need to delete selection otherwise we would fix the current position
                        self.delete(self.position, tkinter.END)
                else: # set position to end so selection starts where textentry ended
                        self.position = len(self.get())
                # collect hits
                _hits = []
                for element in self._completion_list:
                        if element.lower().startswith(self.get().lower()): # Match case insensitively
                                _hits.append(element)
                # if we have a new hit list, keep this in mind
                if _hits != self._hits:
                        self._hit_index = 0
                        self._hits=_hits
                # only allow cycling if we are in a known hit list
                if _hits == self._hits and self._hits:
                        self._hit_index = (self._hit_index + delta) % len(self._hits)
                # now finally perform the auto completion
                if self._hits:
                        self.delete(0,tkinter.END)
                        self.insert(0,self._hits[self._hit_index])
                        self.select_range(self.position,tkinter.END)

        def handle_keyrelease(self, event):
                """event handler for the keyrelease event on this widget"""
                if event.keysym == "BackSpace":
                        self.delete(self.index(tkinter.INSERT), tkinter.END)
                        self.position = self.index(tkinter.END)
                if event.keysym == "Left":
                        if self.position < self.index(tkinter.END): # delete the selection
                                self.delete(self.position, tkinter.END)
                        else:
                                self.position = self.position-1 # delete one character
                                self.delete(self.position, tkinter.END)
                if event.keysym == "Right":
                        self.position = self.index(tkinter.END) # go to end (no selection)
                if len(event.keysym) == 1:
                        self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

        def set_completion_list(self, completion_list):
                """Use our completion list as our drop down selection menu, arrows move through menu."""
                self._completion_list = sorted(completion_list, key=str.lower) # Work with a sorted list
                self._hits = []
                self._hit_index = 0
                self.position = 0
                self.bind('<KeyRelease>', self.handle_keyrelease)
                self['values'] = self._completion_list  # Setup our popup menu




# def test(test_list):
#         """Run a mini application to test the AutocompleteEntry Widget."""
#         root = tkinter.Tk(className=' AutocompleteEntry demo')
#         combo = AutocompleteCombobox(root)
#         combo.set_completion_list(test_list)
#         combo.pack()
#         combo.focus_set()
#         # I used a tiling WM with no controls, added a shortcut to quit
#         root.bind('<Control-Q>', lambda event=None: root.destroy())
#         root.bind('<Control-q>', lambda event=None: root.destroy())
#         root.mainloop()

# if __name__ == '__main__':
#         test_list = ('apple', 'banana', 'CranBerry', 'dogwood', 'alpha', 'Acorn', 'Anise' )
#         test(test_list)