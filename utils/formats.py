def to_codeblock(content, language='py', replace_existing=True, escape_md=True, new="'''"):
    if replace_existing:
        content = content.replace('```', new)
    if escape_md:
        content = escape_md(content)
    return f'```{language}\n{content}\n```'
