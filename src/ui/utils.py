from PIL import Image, ImageTk
import ttkbootstrap as tb

class BackgroundManager:
    def __init__(self, root, image_path, resize_content=True):
        """
        Sets up a responsive background image on the given root window (or Toplevel).
        Creates a central 'content_frame' where the main UI should be placed.
        resize_content: If True, forces the content_frame to fill the window (with margins).
                        If False, allows the content_frame to shrink-wrap its widgets.
        """
        self.root = root
        self.original_image = Image.open(image_path)
        self.photo = None
        self.resize_content = resize_content

        # Create Canvas to hold the image
        self.canvas = tb.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Create a container frame for the app content
        # We use a Labelframe or Frame. Labelframe with text="" gives a nice border/background.
        # bootstyle="default" uses the theme's background (usually white in Flatly).
        self.content_frame = tb.Frame(self.canvas, padding=20, bootstyle="default")
        
        # Place the content frame on the canvas
        self.window_id = self.canvas.create_window(
            0, 0, window=self.content_frame, anchor="center"
        )

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)
        
        # Force initial update
        self.root.after(100, self.force_update)

    def force_update(self):
        """Force an update using current window dimensions."""
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        # Even if w/h are small (1x1), let's try to update if > 1 to catch startup state
        if w > 1 and h > 1:
            self._update_bg(w, h)
        else:
            # Retry if window is not yet ready
            self.root.after(100, self.force_update)

    def on_resize(self, event):
        """Resize background image and center the content frame."""
        # Only handle the root window resize
        if event.widget == self.root:
            self._update_bg(event.width, event.height)

    def _update_bg(self, w, h):
        if w < 50 or h < 50:
            return

        # Resize the image
        resized = self.original_image.resize((w, h), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(resized)

        # Update background
        self.canvas.delete("bg_img")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw", tags="bg_img")
        self.canvas.tag_lower("bg_img")

        # Center the content frame
        self.canvas.coords(self.window_id, w // 2, h // 2)
        
        if self.resize_content:
            # Resize content frame to be responsive (window size minus margins)
            # This ensures inner widgets like ScrolledText can expand properly
            card_w = max(w - 80, 400) # Minimum width safety
            card_h = max(h - 80, 300) # Minimum height safety
            self.canvas.itemconfigure(self.window_id, width=card_w, height=card_h)

    def get_content_frame(self):
        return self.content_frame
