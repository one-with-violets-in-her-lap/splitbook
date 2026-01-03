import click

_WAVEFORM_FRAMES = [
    "\n".join([click.style(line, bold=True) for line in frame.splitlines()])
    for frame in [
        """

 -------- 
----------
 -------- 

    """,
        """

   ----   
 -------- 
   ----   

    """,
        """
    --    
   ----   
----------
   ----   
    --    
    """,
        """
          
 --    -- 
----------
 --    -- 
          
    """,
        """
          
  ------  
----  ----
  ------  
          
    """,
        """
    --    
   ----   
----------
   ----   
    --    
    """,
        """
   ----   
  ------  
----------
  ------  
   ----   
    """,
    ]
]


class CliWaveformAnimation:
    def __init__(self):
        self.line_count = _WAVEFORM_FRAMES[0].count("\n") + 1
        self._current_frame_index = 0

    def get_current_frame_and_update(self):
        current_frame = _WAVEFORM_FRAMES[self._current_frame_index]

        new_frame_index = self._current_frame_index + 1
        if new_frame_index >= len(_WAVEFORM_FRAMES):
            new_frame_index = 0
        self._current_frame_index = new_frame_index

        return current_frame
