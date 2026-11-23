"""Apply an explicitly enabled environment layer at configuration load time."""

import os
import re


def apply_environment(config):
    """Overlay known scalar names without discovering arbitrary environment keys."""
    from . import Section

    prefix = config.env_vars_prefix
    separator = config.env_vars_section_separator
    if not isinstance(prefix, str) or not isinstance(separator, str):
        raise TypeError('Environment prefix and section separator must be strings')
    environment = dict(os.environ)

    def environment_name(parts):
        parts = [re.sub(r'[^a-zA-Z0-9_]', '_', part) for part in parts]
        name = re.sub(r'[^a-zA-Z0-9_]', '_', prefix + separator.join(parts))
        if name and name[0].isdigit():
            name = '_' + name
        return name.upper() if config.env_vars_uppercase else name

    def overlay(section, spec, parents):
        scalars = list(section.scalars)
        if isinstance(spec, Section):
            scalars.extend(name for name in spec.scalars
                           if name not in scalars and name not in ('__many__', '___many___'))
        for name in scalars:
            if name in section.sections:
                continue
            variable = environment_name(parents + [name])
            if variable in environment:
                # Values stay complete strings: commas, hashes and newlines in
                # a secret are data, not config-file syntax. validate() performs
                # the same explicit type conversion as for other input values.
                section[name] = environment[variable]

        sections = list(section.sections)
        if isinstance(spec, Section):
            sections.extend(name for name in spec.sections
                            if name not in sections and name != '__many__')
            many = dict.get(spec, '__many__')
        else:
            many = None
        for name in sections:
            child_spec = dict.get(spec, name, many) if isinstance(spec, Section) else None
            if name in section:
                child = dict.__getitem__(section, name)
                if isinstance(child, Section):
                    overlay(child, child_spec, parents + [name])
                continue
            child = Section(section, section.depth + 1, config, name=name)
            overlay(child, child_spec, parents + [name])
            if child:
                section[name] = child

    overlay(config, config.configspec, [])
