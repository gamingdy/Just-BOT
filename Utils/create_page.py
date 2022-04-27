def generate_page(embed, field_name: list, field_value: list):
    for name, value in zip(field_name, field_value):
        embed.add_field(name=name, value=value, inline=False)
