def copy_canvas(src_canvas, dest_canvas):
    
    # Loop through all items in the source canvas
    for item in src_canvas.find_all():
        coords = src_canvas.coords(item)
        item_type = src_canvas.type(item)
        options = src_canvas.itemconfig(item)
        
        # Extract current configuration (like fill, outline, etc.)
        kwargs = {}
        for key, val in options.items():
            # itemconfig returns a tuple (option, option, default, current_value)
            kwargs[key] = val[-1]  

        # Draw the same item on destination canvas
        if item_type == "rectangle":
            dest_canvas.create_rectangle(*coords, **kwargs)
        elif item_type == "oval":
            dest_canvas.create_oval(*coords, **kwargs)
        elif item_type == "line":
            dest_canvas.create_line(*coords, **kwargs)
        elif item_type == "text":
            dest_canvas.create_text(*coords, **kwargs)
        elif item_type == "polygon":
            dest_canvas.create_polygon(*coords, **kwargs)
