def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.strip().split("\n\n")
    blocks = []

    for block in raw_blocks:
        # Strip each line in the block individually, then rejoin
        cleaned_lines = [line.strip() for line in block.strip().splitlines()]
        cleaned_block = "\n".join(cleaned_lines)
        if cleaned_block:
            blocks.append(cleaned_block)

    return blocks
