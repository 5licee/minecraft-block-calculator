import json
import os
import tkinter
from tkinter import ttk
from typing import List


def get_blocks() -> List[str]:
    """
    Gets all blocks from the blocks folder.
    """
    return [block[:-4] for block in os.listdir('assets/blocks')]


def formatted_quantity(quantity: int) -> str:
    """
    Formats the quantity to have a comma in the right place.
    """
    return f"{quantity//64} stacks + {quantity%64} block(s)"


class CustomEntry(tkinter.Entry):
    """
    Custom entry class.
    """
    def __init__(self, *args, **kwargs):
        kwargs["borderwidth"] = 0
        super().__init__(*args, **kwargs)
        separator = ttk.Separator(orient="horizontal")
        separator.place(in_=self, x=0, rely=1.0, height=2, relwidth=1.0)


class Application:
    def __init__(self):
        """
        Initializes the application.
        """
        self.root = tkinter.Tk()
        self.root.title("minecraft calculator")
        self.root.geometry("900x500")
        self.root.resizable(False, False)

        # var
        self.blocks = get_blocks()
        self.data = []

    def _main(self):
        """
        Constructs the main window.
        """
        main = tkinter.Frame(self.root, width=900, height=500)
        main.configure(background="#000000")
        main.pack()
        main.pack_propagate(0)

        # components
        def _canvas():
            # holder
            canvas_holder = tkinter.Frame(main, width=650, height=450)
            canvas_holder.configure(background="#111111")
            canvas_holder.place(x=0, y=0)
            canvas_holder.pack_propagate(0)

            # canvas
            self.canvas = tkinter.Canvas(canvas_holder, width=635, height=450)
            self.canvas.configure(background="#111111", highlightthickness=0)
            self.canvas.pack(side="left", fill="both", expand=True)
            self.canvas.pack_propagate(0)

            # scrollbar
            scrollbar = tkinter.Scrollbar(canvas_holder, width=15)
            scrollbar.configure(command=self.canvas.yview, orient="vertical")
            scrollbar.pack(side="right", fill="y")

            # binds
            self.canvas.configure(yscrollcommand=scrollbar.set)
            self.canvas.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        def _menu():
            # background
            image = tkinter.PhotoImage(file='assets/dirt-background.png')
            background = tkinter.Label(main, width=250, height=450, image=image)
            background.image = image
            background.place(x=650, y=0)

            # menu
            menu_holder = tkinter.Frame(main, width=250, height=100)
            menu_holder.configure(background="#222222")
            menu_holder.place(x=650, y=0)
            menu_holder.pack_propagate(0)

            # buttons
            for name in ["[clear-all]", "[quit]"]:
                # holder 
                button_holder = tkinter.Frame(menu_holder, width=250, height=50)
                button_holder.configure(background="#222222")
                button_holder.pack(side="top", fill="x")
                button_holder.pack_propagate(0)

                # button
                button = tkinter.Label(button_holder, text=name)
                button.configure(background="#222222", foreground="#ffffff", font="monaco 12")
                button.pack(side="top", fill="x", pady=12)

                # binds
                if name == "[clear-all]": button.bind("<Button-1>", lambda event: self.event_handler("clear-all"))
                elif name == "[quit]": button.bind("<Button-1>", lambda event: self.event_handler("quit"))
                button.bind("<Enter>", lambda event: event.widget.configure(foreground="#ff0000"))
                button.bind("<Leave>", lambda event: event.widget.configure(foreground="#ffffff"))

        def _input():
            # holder
            input_holder = tkinter.Frame(main, width=900, height=50)
            input_holder.configure(background="#333333")
            input_holder.place(x=0, y=450)
            input_holder.pack_propagate(0)

            # input
            self.input = CustomEntry(input_holder)
            self.input.configure(background="#333333", foreground="#ffffff", font="monaco 12", insertbackground="#ffffff")
            self.input.pack(side="left", fill="x", expand=True, padx=(25, 0), pady=(12, 0))

            # binds
            self.input.bind("<Return>", lambda event: self.event_handler("input"))

            # button
            button = tkinter.Label(input_holder, text="[enter]")
            button.configure(background="#333333", foreground="#ffffff", font="monaco 12")
            button.pack(side="left", fill="x", padx=(0, 250), pady=12)

            # binds
            button.bind("<Button-1>", lambda event: self.event_handler("input"))
            button.bind("<Enter>", lambda event: event.widget.configure(foreground="#ff0000"))
            button.bind("<Leave>", lambda event: event.widget.configure(foreground="#ffffff"))


        # build
        _canvas()
        _menu()
        _input()

    def _update(self):
        """
        Updates the canvas.
        """
        
        # clear
        self.canvas.delete("all")

        # get data
        with open("data.json", "r") as f:
            try:
                self.data = json.load(f)
            except json.decoder.JSONDecodeError:
                self.data = []
                return
        
        # components
        def _canvasframe(block, quantity) -> tkinter.Frame:
            # holder
            frame = tkinter.Frame(self.canvas, width=635, height=50)
            frame.configure(background="#111111")
            frame.pack(side="top", fill="x")
            frame.pack_propagate(0)

            # icon
            icon = tkinter.Canvas(frame, width=25, height=25)        
            icon.configure(background="#111111", highlightthickness=0)
            icon.pack(side="left", padx=25, pady=12)

            if block in self.blocks:
                image = tkinter.PhotoImage(file='assets/blocks/' + block + '.png').zoom(2)
            else:
                image = tkinter.PhotoImage(file='assets/blocks/unknown.png')
            
            icon.create_image(0, 0, anchor="nw", image=image)
            icon.image = image
            
            # text block
            text = tkinter.Label(frame, text=f"{block.replace('_', ' ').title():15} ")
            text.configure(background="#111111", foreground="#ffffff", font="monaco 12")
            text.pack(side="left")

            if len(block) > 15: text.configure(font="monaco 10")
            if len(block) > 20: text.configure(font="monaco 8")
            
            # text quantity
            text = tkinter.Label(frame, text=f"{formatted_quantity(int(quantity))}")
            text.configure(background="#111111", foreground="#ffffff", font="monaco 12")
            text.pack(side="left")

            # delete
            delete = tkinter.Label(frame, text="[delete]")
            delete.configure(background="#111111", foreground="#ffffff", font="monaco 12")
            delete.pack(side="right", padx=25)
            delete.bind("<Button-1>", lambda event: self.event_handler("delete", block))
            delete.bind("<Enter>", lambda event: delete.configure(foreground="#ff0000"))
            delete.bind("<Leave>", lambda event: delete.configure(foreground="#ffffff"))

            # binds
            if len(self.data) > 8:
                frame.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
                icon.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
                text.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

            return frame

        # build
        for i, value in enumerate(self.data):
            frame = _canvasframe(value["block"], value["quantity"])
            self.canvas.create_window(0, i * 54, window=frame, anchor="nw")
            if i == 0: 
                self.canvas.create_line(30, 52, 600, 52, fill="#ffffff", width=1)
            else: 
                self.canvas.create_line(30, i*54+52, 600, i*54+52, fill="#ffffff", width=1)

        # scroll config
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(1)
        if len(self.data) > 8:
            self.canvas.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def event_handler(self, event: str, *args):
        """
        Handles events.
        """

        if event == "input":
            # get value        
            value = self.input.get()
            # check for blank
            if value == "":
                return
            try:
                # check for format
                quantity, *block = value.split(" ")
                quantity = int(quantity)
                block = "_".join(block)

                # get data
                with open("data.json", "r") as f:
                    self.data = json.load(f)

                # dump data
                with open("data.json", "w") as f:
                    self.data.append({"block": block, "quantity": quantity})
                    json.dump(self.data, f, indent=4)
                
                # update canvas
                self._update()

                # clear
                self.input.delete(0, "end")

            except ValueError:
                return
    
        elif event == "clear-all":
            # delete data
            with open("data.json", "w") as f:
                json.dump([], f, indent=4)
            
            # update canvas
            self._update()

        elif event == "delete":
            # get data
            with open("data.json", "r") as f:
                self.data = json.load(f)

            # remove item
            self.data = [x for x in self.data if x["block"] != args[0]]

            # dump data
            with open("data.json", "w") as f:
                json.dump(self.data, f, indent=4)

            # update canvas
            self._update()

        elif event == "quit":
            self.root.destroy()

    def run(self):
        """
        Runs the Application.
        """
        self._main()
        self._update()
        self.root.mainloop()


def main() -> int:
    """
    Main function.
    """

    # init
    app = Application()
    app.run()

    # return
    return 0


if __name__ == "__main__":
    main()
