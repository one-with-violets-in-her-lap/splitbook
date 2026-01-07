# Splitbook

Tool for generating timecodes for large audiobooks which do not have any chapter metadata in them

It transcribes the book with [Whisper](https://github.com/openai/whisper) and searches
for marker words, like "Unit 1", using regex patterns (I know it sucks and should be more user-friendly)

You can split the book into multiple audio files or save the timecodes in a single MP3 file via ID3 tags

![](./showcase.gif)

## Usage

Install with pip:

```sh
pip install git+https://github.com/one-with-violets-in-her-lap/splitbook
```

Run the program:

```sh
python -m splitbook <Audio file> --search <Search regex for matching marker words> [...other options]
```

There are other useful options like Whisper model size (small/medium/etc) and language, which can be discovered using:
`splitbook --help`

### Search patterns

Search patterns are specified in case-insensitive regex format

#### Examples:

- Numbered chapters (e.g. "Unit 1", "Unit 2"):

  ```sh
  splitbook ./book.mp3 --search "Unit \d+"
  ```

- Identifying lettered sections (e.g. "Exercise A", "Exercise C"):

  ```sh
  splitbook ./book.mp3 --search "Exercise [A-Z]"
  ```

- Multiple patterns:
  ```sh
  splitbook ./book.mp3 --search "Exercise [A-Z]" --search "Unit \d+"
  ```

### Whisper model selection

`splitbook` uses Whisper which [supports different model sizes](https://github.com/openai/whisper?tab=readme-ov-file#available-models-and-languages):

```bash
python -m splitbook ./book.mp3 --search "Chapter \d+" --model small
```
