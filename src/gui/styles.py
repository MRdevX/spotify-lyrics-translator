"""GUI styles configuration."""

import tkinter.ttk as ttk

def configure_styles(style: ttk.Style) -> None:
    """Configure custom styles for the application."""
    style.configure(
        "Song.TLabel",
        font=('Helvetica', 14, 'bold'),
        foreground='#1DB954'  # Spotify green
    )
    
    style.configure(
        "Info.TLabel",
        font=('Helvetica', 10),
        foreground='#B3B3B3'  # Spotify light gray
    )
    
    style.configure(
        "Treeview",
        font=('Helvetica', 11),
        rowheight=30,
        background='#282828',
        foreground='#FFFFFF',
        fieldbackground='#282828',
        borderwidth=0,
        dividerwidth=2,
        dividercolor='#404040'
    )
    
    style.configure(
        "Treeview.Heading",
        font=('Helvetica', 12, 'bold'),
        background='#1DB954',
        foreground='white'
    )
    
    style.map(
        'Treeview',
        background=[('selected', '#1DB954')],
        foreground=[('selected', 'white')]
    )
    
    style.configure(
        "Spotify.Horizontal.TProgressbar",
        troughcolor='#404040',
        background='#1DB954',
        darkcolor='#1DB954',
        lightcolor='#1DB954'
    ) 