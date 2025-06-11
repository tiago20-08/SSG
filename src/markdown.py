def markdown_to_blocks(markdown):
    parr = (markdown.split("\n\n"))
    res = []
    for line in parr:
        res.append(line.strip())
    
    return res