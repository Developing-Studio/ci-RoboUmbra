from discord.utils import escape_markdown

def to_codeblock(content, language='py', replace_existing=True, escape_md=True, new="'''"):
    if replace_existing:
        content = content.replace('```', new)
    if escape_md:
        content = escape_markdown(content)
    return f'```{language}\n{content}\n```'
