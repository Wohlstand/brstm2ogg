# BRSTM to OGG converter

This is a very simple command-line tool that runs `vgmstream-cli` and `oggenc`
in order to convert BRSTM and other supported formats into OGG files with
keeping of loop tags as Vorbis comments. Such way of looping in OGG files is
used at various software like RPG Maker, SDL_mixer, GZDoom, etc.

## Dependencies
- Python 3.x
- VGMStream (`vgmstream-cli`) being available in the PATH environment: https://github.com/vgmstream/vgmstream
- `oggenc` utility (`vobris-tools` package is needed) being available in the PATH environment: https://github.com/xiph/vorbis-tools

## Syntax:
```
   ./brstm2ogg.py <input file> [<output file>]
```

or:
```
   python3 brstm2ogg.py <input file> [<output file>]
```

- `<input file>` - **Required** the full path to the input file to convert.
- `<output file>` - **Optional** the output file path. If not specified, the output file will be saved at the same directory as input file.
