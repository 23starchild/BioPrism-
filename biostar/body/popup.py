from datetime import date

import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

from biostar.modules.data import (
    ANALOGY_COMPONENTS_AREAS,
    ANALOGY_TREE_AREAS,
    COMPONENT_TYPES,
    PROCESSING_TECHNIQUES,
    SAMPLING_DEVICE_TYPE_MAP,
    SPEC_ISO_CLASSES,
    TABLE_DEF_PPEL,
    TABLE_DEF_SAMPLES,
)

CONFIGURE_SAMPLE_MODAL = dmc.Modal(
    id="modal-configure-sample",
    title=dmc.Flex(
        justify="space-between",
        align="center",
        children=[
            dmc.Text("Configure Sample", fw=500),
            dmc.Flex(
                justify="end",
                gap="xs",
                children=[
                    dmc.Button(
                        "Apply Changes",
                        id="button-configure-sample-apply",
                        size="xs",
                        color="violet",
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:close", width=16),
                        id="button-configure-sample-close",
                        size="md",
                        color="red",
                        variant="light",
                    ),
                ],
            ),
        ],
    ),
    size=None,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    keepMounted=True,
    styles={
        "header": {"backgroundColor": "var(--mantine-color-gray-2)", "paddingRight": 16},
        "title": {"width": "100%"},
        "inner": {
            "paddingLeft": 17,
            "paddingRight": 17,
            "paddingTop": 153,
            "paddingBottom": 86,
            "justifyContent": "flex-start",
        },
    },
    children=[
        dmc.Center(
            "REQUIRED INPUTS",
            style={"borderBottom": "1px solid var(--mantine-color-gray-5)"},
            c="gray.6",
            mb=4,
            mt=12,
        ),
        dmc.Select(
            id="select-configure-sample-id",
            mb=4,
            mt=8,
            label="Sample ID",
            disabled=True,
            value=None,
            data=[],
        ),
        dmc.Select(
            id="select-configure-sample-hardware-id",
            mb=4,
            label="Sampled Hardware ID",
            disabled=True,
            value=None,
            data=[],
        ),
        dmc.Select(
            id="select-configure-sample-accountable",
            data=[
                {"label": "Yes", "value": "Yes"},
                {"label": "No", "value": "No"},
            ],
            value="Yes",
            mb=4,
            label="PP Accountable",
            description="Non-accountable samples will be recorded in the tool but ignored for all bioburden calculations",
            allowDeselect=False,
        ),
        dmc.Flex(
            justify="space-between",
            gap="sm",
            children=[
                dmc.Select(
                    id="select-configure-sample-device",
                    data=[{"label": opt, "value": opt} for opt in ["Swab", "Wipe"]],
                    value="Swab",
                    w="100%",
                    placeholder="Select one...",
                    label="Sampling Device",
                    allowDeselect=False,
                ),
                dmc.Select(
                    id="select-configure-sample-device-type",
                    w="100%",
                    data=SAMPLING_DEVICE_TYPE_MAP["Swab"],
                    value="Puritan Cotton",
                    placeholder="Select one...",
                    label="Sampling Device Type",
                    allowDeselect=False,
                ),
            ],
            mb=4,
        ),
        dmc.Select(
            id="select-configure-sample-technique",
            data=PROCESSING_TECHNIQUES,
            value="NASA Standard",
            mb=4,
            placeholder="Select one...",
            label="Processing Technique",
            allowDeselect=False,
        ),
        dmc.NumberInput(
            id="input-configure-sample-area-volume",
            min=0,
            step=0.1,
            mb=4,
            label="Sampled Area (m²)",
        ),
        dmc.NumberInput(
            id="input-configure-sample-fraction",
            value=1,
            min=0,
            max=1,
            step=0.1,
            mb=4,
            label="Pour Fraction",
            description="Defaults provided but feel free to change for your sample",
        ),
        dmc.NumberInput(
            id="input-configure-sample-cfu",
            min=0,
            step=1,
            allowDecimal=False,
            mb=12,
            label="CFU",
            description="Total colony forming units observed across all dishes",
        ),
        dmc.Center(
            "METADATA",
            style={"borderBottom": "1px solid var(--mantine-color-gray-5)"},
            c="gray.6",
            mb=4,
        ),
        dmc.Flex(
            justify="space-between",
            gap="sm",
            children=[
                dmc.TextInput(
                    id="input-configure-sample-assay-name",
                    label="Assay Name",
                    w="100%",
                ),
                dmc.DateInput(
                    id="input-configure-sample-assay-date",
                    valueFormat="YYYY-MM-DD",
                    value=date.today(),
                    w="100%",
                    label="Assay Date",
                ),
            ],
            mb=4,
        ),
        dmc.Flex(
            justify="space-between",
            gap="sm",
            mb=4,
            children=[
                dmc.TextInput(
                    id="input-configure-sample-pp-cert",
                    label="PP Cert #",
                    w="100%",
                ),
                dmc.Select(
                    id="select-configure-sample-control",
                    data=[
                        "Facility Control",
                        "Negative Control",
                        "Positive Control",
                        "Field Control",
                        "Other Control",
                        "Not Control",
                    ],
                    value="Not Control",
                    label="Control Type",
                    allowDeselect=False,
                    w="100%",
                ),
            ],
        ),
        dmc.Textarea(
            id="input-configure-sample-notes",
            label="Sampling Notes",
            required=False,
        ),
    ],
)

CONFIGURE_HARDWARE_MODAL = dmc.Modal(
    id="modal-configure-hardware",
    title=dmc.Flex(
        justify="space-between",
        align="center",
        children=[
            dmc.Text("Configure Hardware", fw=500),
            dmc.Flex(
                justify="end",
                gap="xs",
                children=[
                    dcc.ConfirmDialog(
                        id="confirm-configure-hardware-delete",
                        message="Are you sure you want to delete this component? This will clear any associated samples and may impact other components.",
                    ),
                    dmc.Button(
                        "Delete",
                        id="button-configure-hardware-delete",
                        size="xs",
                        color="red.5",
                    ),
                    dmc.Button(
                        "Apply Changes",
                        id="button-configure-hardware-apply",
                        size="xs",
                        color="violet",
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:close", width=16),
                        id="button-configure-hardware-close",
                        size="md",
                        color="red",
                        variant="light",
                    ),
                ],
            ),
        ],
    ),
    size=None,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    keepMounted=True,
    styles={
        "header": {"backgroundColor": "var(--mantine-color-gray-2)", "paddingRight": 16},
        "title": {"width": "100%"},
        "inner": {
            "paddingLeft": 17,
            "paddingRight": 17,
            "paddingTop": 153,
            "paddingBottom": 86,
            "justifyContent": "flex-start",
        },
    },
    children=[
        dmc.Center(
            "REQUIRED INPUTS",
            style={"borderBottom": "1px solid var(--mantine-color-gray-5)"},
            c="gray.6",
            mb=4,
            mt=12,
        ),
        dmc.Select(
            label="Hardware ID",
            id="select-configure-hardware-id",
            disabled=True,
            w="100%",
            mb=4,
            mt=8,
            value=None,
            data=[],
        ),
        dmc.Flex(
            justify="space-between",
            gap="sm",
            children=[
                dmc.Select(
                    id="select-hardware-group",
                    data=[],
                    value=None,
                    clearable=True,
                    w="100%",
                    placeholder="Select one...",
                    label="Group",
                    description="Tag for the created group",
                ),
                dmc.NumberInput(
                    id="input-hardware-group-density-2d",
                    min=0,
                    step=0.1,
                    disabled=True,
                    value="",
                    w="100%",
                    label="Target Density (2D)",
                    description="For areas (spores / m²)",
                ),
                dmc.NumberInput(
                    id="input-hardware-group-density-3d",
                    min=0,
                    step=0.1,
                    disabled=True,
                    value="",
                    w="100%",
                    label="Target Density (3D)",
                    description="For volumes (spores / cm³)",
                ),
            ],
        ),
        html.Div(
            id="container-inputs-component",
            style={"display": "none", "marginTop": "4px"},
            children=[
                dmc.Flex(
                    justify="space-between",
                    gap="sm",
                    mb=4,
                    children=[
                        dmc.Select(
                            id="select-hardware-dim",
                            data=[
                                {"label": opt, "value": opt} for opt in ["2D (Area)", "3D (Volume)"]
                            ],
                            value="2D (Area)",
                            allowDeselect=False,
                            w="100%",
                            label="Component Dimensionality",
                        ),
                        dmc.NumberInput(
                            id="input-hardware-area-volume",
                            debounce=True,
                            min=0,
                            step=1,
                            w="100%",
                            label="Total Area (m²)",
                        ),
                    ],
                ),
                dmc.Select(
                    id="select-hardware-type",
                    data=[{"label": opt, "value": opt} for opt in COMPONENT_TYPES],
                    value=None,
                    clearable=True,
                    mb=4,
                    label="Component Type",
                ),
                html.Div(
                    id="container-inputs-sampled",
                    style={"display": "none"},
                    children=[
                        dmc.Select(
                            id="select-hardware-analogy",
                            data=ANALOGY_COMPONENTS_AREAS,
                            placeholder="Select one...",
                            clearable=False,
                            allowDeselect=False,
                            searchable=True,
                            label="Analogy",
                            description="Select an analogy to provide a prior for this component; expand the tree below to explore the hierarchy of options or select a specific analogy to see its metadata",
                        ),
                        dmc.Flex(
                            justify="start",
                            gap="md",
                            style={"width": "100%"},
                            wrap="wrap",
                            children=[
                                dmc.Tree(
                                    id="tree-hardware-analogy",
                                    mt=8,
                                    data=ANALOGY_TREE_AREAS,
                                    # checkboxes=True,
                                    # allowRangeSelection=False,
                                    levelOffset="xl",
                                    styles={"label": {"fontSize": "var(--mantine-font-size-sm)"}},
                                    style={
                                        "minWidth": "25%",
                                        "width": "maxcontent",
                                        "maxWidth": "100%",
                                        "flex": "0 0 auto",
                                    },
                                ),
                                html.Div(
                                    style={
                                        "flex": "1 1 50%",
                                        "minWidth": "50%",
                                        "marginTop": "4px",
                                    },
                                    children=[
                                        dmc.Text(
                                            [
                                                html.B("Handling Constraints: "),
                                                html.Span("-", id="analogy-handling"),
                                            ],
                                            fz=12,
                                            mt=8,
                                        ),
                                        dmc.Text(
                                            [
                                                html.B("Ventilation: "),
                                                html.Span("-", id="analogy-ventilation"),
                                            ],
                                            fz=12,
                                        ),
                                        dmc.Text(
                                            [
                                                html.B("Material Composition: "),
                                                html.Span("-", id="analogy-composition"),
                                            ],
                                            fz=12,
                                        ),
                                        dmc.Text(
                                            [html.B("Notes: "), html.Span("-", id="analogy-notes")],
                                            fz=12,
                                            mb=8,
                                        ),
                                        dmc.Table(
                                            [
                                                dmc.TableThead(
                                                    dmc.TableTr(
                                                        [
                                                            dmc.TableTh("Phase"),
                                                            dmc.TableTh("Cleaning Procedures"),
                                                            dmc.TableTh("Bioburden Reduction"),
                                                        ]
                                                    )
                                                ),
                                                dmc.TableTbody(
                                                    [
                                                        dmc.TableTr(
                                                            [
                                                                dmc.TableTd("Fabrication"),
                                                                dmc.TableTd(
                                                                    "-", id="analogy-cleaning-fab"
                                                                ),
                                                                dmc.TableTd(
                                                                    "-", id="analogy-reduction-fab"
                                                                ),
                                                            ]
                                                        ),
                                                        dmc.TableTr(
                                                            [
                                                                dmc.TableTd("Pre-SI&T"),
                                                                dmc.TableTd(
                                                                    "-", id="analogy-cleaning-pre"
                                                                ),
                                                                dmc.TableTd(
                                                                    "-", id="analogy-reduction-pre"
                                                                ),
                                                            ]
                                                        ),
                                                        dmc.TableTr(
                                                            [
                                                                dmc.TableTd("SI&T"),
                                                                dmc.TableTd(
                                                                    "-", id="analogy-cleaning-sit"
                                                                ),
                                                                dmc.TableTd(
                                                                    "-", id="analogy-reduction-sit"
                                                                ),
                                                            ]
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            fz=12,
                                            style={
                                                "borderTop": "1px dashed var(--mantine-color-gray-5)"
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="container-inputs-implied",
                    style={"display": "none"},
                    children=dmc.Select(
                        id="select-hardware-implied-id",
                        placeholder="Select one...",
                        clearable=True,
                        label="Origin",
                        description="Pointer to another component whose bioburden should be assumed here",
                    ),
                ),
                html.Div(
                    id="container-inputs-spec",
                    style={"display": "none"},
                    children=dmc.Flex(
                        justify="space-between",
                        gap="sm",
                        children=[
                            dmc.Select(
                                id="select-hardware-spec",
                                data=[
                                    {"label": opt, "value": opt}
                                    for opt in SPEC_ISO_CLASSES["2D (Area)"]
                                ],
                                placeholder="Select one...",
                                label="Facility ISO Class",
                                w="100%",
                                clearable=True,
                            ),
                            dmc.NumberInput(
                                id="input-hardware-spec-density",
                                min=0,
                                disabled=True,
                                label="Density Spec",
                            ),
                        ],
                    ),
                ),
            ],
        ),
        dmc.Center(
            "METADATA",
            style={"borderBottom": "1px solid var(--mantine-color-gray-5)"},
            c="gray.6",
            mb=4,
            mt=12,
        ),
        dmc.TextInput(
            id="input-hardware-handling",
            label="Handling Constraints",
            description="Brief characterization of hardware constraints; what cannot be cleaned or sampled",
            mb=4,
        ),
        dmc.TextInput(
            id="input-hardware-ventilation",
            label="Ventilation",
            description="Brief characterization of hardware ventilation",
            mb=4,
        ),
        dmc.TextInput(
            id="input-hardware-composition",
            label="Material Composition",
            description="Brief characterization of hardware material type",
            mb=4,
        ),
        dmc.Grid(
            justify="start",
            align="stretch",
            gutter="sm",
            mb=4,
            children=[
                dmc.GridCol(
                    dmc.NumberInput(
                        id="input-hardware-reduction-fab",
                        label="Cleaning & Bioburden Reduction (Fabrication)",
                        description="(Below) orders of magnitude reduction from fabrication cleaning procedures (Right) Brief description of cleaning procedures undergone",
                        min=0,
                    ),
                    span=7,
                ),
                dmc.GridCol(
                    dmc.Textarea(
                        id="input-hardware-cleaning-fab",
                        required=False,
                        styles={
                            "root": {"height": "100%"},
                            "wrapper": {"height": "100%", "paddingTop": "6px"},
                            "input": {"height": "100%"},
                        },
                    ),
                    span=5,
                ),
            ],
        ),
        dmc.Grid(
            justify="start",
            align="stretch",
            gutter="sm",
            mb=4,
            children=[
                dmc.GridCol(
                    dmc.NumberInput(
                        id="input-hardware-reduction-pre",
                        label="Cleaning & Bioburden Reduction (Pre-SI&T)",
                        description="(Below) orders of magnitude reduction from pre-SI&T cleaning procedures (Right) Brief description of cleaning procedures undergone",
                        min=0,
                    ),
                    span=7,
                ),
                dmc.GridCol(
                    dmc.Textarea(
                        id="input-hardware-cleaning-pre",
                        required=False,
                        styles={
                            "root": {"height": "100%"},
                            "wrapper": {"height": "100%", "paddingTop": "6px"},
                            "input": {"height": "100%"},
                        },
                    ),
                    span=5,
                ),
            ],
        ),
        dmc.Grid(
            justify="start",
            align="stretch",
            gutter="sm",
            mb=4,
            children=[
                dmc.GridCol(
                    dmc.NumberInput(
                        id="input-hardware-reduction-sit",
                        label="Cleaning & Bioburden Reduction (SI&T)",
                        description="(Below) orders of magnitude reduction from SI&T cleaning procedures (Right) brief description of cleaning procedures undergone",
                        min=0,
                    ),
                    span=7,
                ),
                dmc.GridCol(
                    dmc.Textarea(
                        id="input-hardware-cleaning-sit",
                        required=False,
                        styles={
                            "root": {"height": "100%"},
                            "wrapper": {"height": "100%", "paddingTop": "6px"},
                            "input": {"height": "100%"},
                        },
                    ),
                    span=5,
                ),
            ],
        ),
        dmc.Textarea(
            id="input-hardware-notes",
            label="Hardware Notes",
            required=False,
        ),
    ],
)

CONFIGURE_PROJECT_MODAL = dmc.Modal(
    id="modal-configure-project",
    title=dmc.Flex(
        justify="space-between",
        align="center",
        children=[
            dmc.Text("Configure Project", fw=500),
            dmc.Flex(
                justify="end",
                gap="xs",
                children=[
                    dmc.Button(
                        "Apply Changes",
                        id="button-configure-project-apply",
                        size="xs",
                        color="violet",
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:close", width=16),
                        id="button-configure-project-close",
                        size="md",
                        color="red",
                        variant="light",
                    ),
                ],
            ),
        ],
    ),
    size=None,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    keepMounted=True,
    styles={
        "header": {"backgroundColor": "var(--mantine-color-gray-2)", "paddingRight": 16},
        "title": {"width": "100%"},
        "inner": {
            "paddingLeft": 17,
            "paddingRight": 17,
            "paddingTop": 153,
            "paddingBottom": 86,
            "justifyContent": "flex-start",
        },
    },
    children=[
        dmc.TextInput(
            label="Project Name",
            description="This will be used for site headers and PPEL exports",
            id="input-project-name",
            mb=4,
            mt=8,
            value="My Project",
        ),
        dmc.Flex(
            justify="space-between",
            gap="sm",
            mb=4,
            children=[
                dmc.Select(
                    id="select-project-group",
                    data=[],
                    value=None,
                    clearable=True,
                    w="100%",
                    placeholder="Select one...",
                    label="Group",
                    description="Tag for the created group",
                ),
                dmc.NumberInput(
                    id="input-project-density-2d",
                    min=0,
                    step=0.1,
                    disabled=True,
                    value="",
                    w="100%",
                    label="Target Density (2D)",
                    description="Target for areas (spores / m²)",
                ),
                dmc.NumberInput(
                    id="input-project-density-3d",
                    min=0,
                    step=0.1,
                    disabled=True,
                    value="",
                    w="100%",
                    label="Target Density (3D)",
                    description="Target for volumes (spores / cm³)",
                ),
            ],
        ),
    ],
)

IMPORT_HARDWARE_MODAL = dmc.Modal(
    id="modal-import-hardware",
    title=dmc.Flex(
        justify="space-between",
        align="center",
        children=[
            dmc.Text("Import Hardware from PPEL", fw=500),
            dmc.Flex(
                justify="end",
                gap="xs",
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:close", width=16),
                        id="button-import-hardware-close",
                        size="md",
                        color="red",
                        variant="light",
                    ),
                ],
            ),
        ],
    ),
    size="lg",
    centered=True,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    keepMounted=True,
    styles={
        "header": {"backgroundColor": "var(--mantine-color-gray-2)", "paddingRight": 16},
        "title": {"width": "100%"},
    },
    children=[
        dmc.Text(
            [
                "Use the buttons below to load hardware from a PPEL file, or to download a template of the appropriate file format. The template is color coded according to the rules in the list below. For long form definitions of each field in the PPEL (including the Samples table), see ",
                html.A(
                    "here",
                    id="link-table-definitions",
                    style={"color": "var(--mantine-color-blue-5)", "cursor": "pointer"},
                ),
                ".",
            ],
            mt=16,
            mb=8,
            fz=14,
        ),
        html.Ul(
            [
                html.Li(
                    [
                        "Required Inputs [RI] (",
                        html.Span("green cells", style={"color": "#51cf66"}),
                        "): used to configure tool results; directly read from the file into the tool",
                    ]
                ),
                html.Li(
                    [
                        "Metadata Only [MDO] (",
                        html.Span("yellow cells", style={"color": "#fcc419"}),
                        "): informational only, do not affect tool results; directly read from the file into the tool",
                    ]
                ),
                html.Li(
                    [
                        "Derived Field [D] (",
                        html.Span("blue cells", style={"color": "#339af0"}),
                        "): autopopulated by tool based on other inputs; skipped during file read process",
                    ]
                ),
                html.Li(
                    [
                        "Ignored (",
                        html.Span("gray cells", style={"color": "#767676"}),
                        "): not relevant or applicable; skipped during the file read process",
                    ]
                ),
            ],
            style={"fontSize": 12, "marginTop": 0, "marginBottom": 0},
        ),
        dmc.Text(
            "Columns not represented in the template are allowed but will be skipped. Warning - the uploaded data will OVERWRITE any existing tool state!",
            mt=8,
            mb=16,
            fz=14,
        ),
        dmc.Grid(
            justify="space-between",
            gutter="sm",
            mb=16,
            children=[
                dmc.GridCol(
                    span=6,
                    children=dcc.Upload(
                        id="upload-import-hardware",
                        max_size=25_000_000,
                        children=dmc.Button("Upload PPEL File", w="100%", color="teal.8"),
                    ),
                ),
                dmc.GridCol(
                    span=6,
                    children=html.A(
                        dmc.Button("Download PPEL Template", w="100%", color="teal.8"),
                        href="/static/biostar/templates/template_ppel.xlsx",
                    ),
                ),
            ],
        ),
        dmc.Center(
            id="filename-import-hardware",
            children="Last Upload: None",
        ),
        html.Div(id="warnings-import-hardware", children=[]),
    ],
)

IMPORT_SAMPLES_MODAL = dmc.Modal(
    id="modal-import-samples",
    title=dmc.Flex(
        justify="space-between",
        align="center",
        children=[
            dmc.Text("Import Samples from PPS", fw=500),
            dmc.Flex(
                justify="end",
                gap="xs",
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:close", width=16),
                        id="button-import-samples-close",
                        size="md",
                        color="red",
                        variant="light",
                    ),
                ],
            ),
        ],
    ),
    size="lg",
    centered=True,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    keepMounted=True,
    styles={
        "header": {"backgroundColor": "var(--mantine-color-gray-2)", "paddingRight": 16},
        "title": {"width": "100%"},
    },
    children=[
        dmc.Text(
            "Use the buttons below to load samples from a PPS file, or to download a template of the appropriate file format. The template is color coded according to the rules in the list below.",
            mt=16,
            mb=8,
            fz=14,
        ),
        html.Ul(
            [
                html.Li(
                    [
                        "Required Inputs [RI] (",
                        html.Span("green cells", style={"color": "#51cf66"}),
                        "): used to configure tool results; directly read from the file into the tool",
                    ]
                ),
                html.Li(
                    [
                        "Metadata Only [MDO] (",
                        html.Span("yellow cells", style={"color": "#fcc419"}),
                        "): informational only, do not affect tool results; directly read from the file into the tool",
                    ]
                ),
                html.Li(
                    [
                        "Ignored (",
                        html.Span("gray cells", style={"color": "#767676"}),
                        "): not relevant or applicable; skipped during the file read process",
                    ]
                ),
            ],
            style={"fontSize": 12, "marginTop": 0, "marginBottom": 0},
        ),
        dmc.Text(
            "Valid uploaded samples will be appended to the current set (no overwrite).",
            mt=8,
            mb=16,
            fz=14,
        ),
        dmc.Grid(
            justify="space-between",
            gutter="sm",
            mb=16,
            children=[
                dmc.GridCol(
                    span=6,
                    children=dcc.Upload(
                        id="upload-import-samples",
                        max_size=25_000_000,
                        children=dmc.Button("Upload PPS File", w="100%", color="teal.8"),
                    ),
                ),
                dmc.GridCol(
                    span=6,
                    children=html.A(
                        dmc.Button("Download PPS Template", w="100%", color="teal.8"),
                        href="/static/biostar/templates/template_pps.xlsx",
                    ),
                ),
            ],
        ),
        dmc.Center(
            id="filename-import-samples",
            children="Last Upload: None",
        ),
        html.Div(id="warnings-import-samples", children=[]),
    ],
)

TABLE_DEFS_MODAL = dmc.Modal(
    id="modal-table-definitions",
    title=dmc.Flex(
        justify="space-between",
        align="center",
        children=[
            dmc.Text("Table Definitions", fw=500),
            dmc.Flex(
                justify="end",
                gap="xs",
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon="carbon:close", width=16),
                        id="button-table-definitions-close",
                        size="md",
                        color="red",
                        variant="light",
                    ),
                ],
            ),
        ],
    ),
    size="80%",
    centered=True,
    withCloseButton=False,
    closeOnClickOutside=False,
    closeOnEscape=False,
    keepMounted=True,
    styles={
        "header": {"backgroundColor": "var(--mantine-color-gray-2)", "paddingRight": 16},
        "title": {"width": "100%"},
    },
    children=dmc.Tabs(
        color="red.5",
        variant="pills",
        value="ppel",
        mt=16,
        children=[
            dmc.TabsList(
                [
                    dmc.TabsTab("PPEL", value="ppel"),
                    dmc.TabsTab("Samples", value="samples"),
                ],
                justify="center",
                grow=True,
                mb=16,
            ),
            dmc.TabsPanel(
                value="ppel",
                children=[
                    dmc.Table(
                        [
                            dmc.TableThead(
                                [
                                    dmc.TableTr(
                                        [
                                            dmc.TableTh("Field Name"),
                                            dmc.TableTh("Description"),
                                            dmc.TableTh("Units"),
                                            dmc.TableTh("Data Type"),
                                            dmc.TableTh("Validation"),
                                            dmc.Tooltip(
                                                dmc.TableTh(
                                                    dmc.Flex(
                                                        justify="start",
                                                        align="center",
                                                        gap=0,
                                                        children=[
                                                            "Field Class",
                                                            DashIconify(
                                                                icon="material-symbols-light:indeterminate-question-box-rounded",
                                                                width=24,
                                                                style={
                                                                    "marginLeft": "4px",
                                                                    "marginTop": "2px",
                                                                },
                                                            ),
                                                        ],
                                                    )
                                                ),
                                                label=html.Ul(
                                                    [
                                                        html.Li(
                                                            "RI: required input; used to configure results and calculations within the BioSTAR interface"
                                                        ),
                                                        html.Li(
                                                            "MDO: metadata only; available for documentation purposes but no impact on tool functionality"
                                                        ),
                                                        html.Li(
                                                            "D: derived field; populated by the tool based on current state of hardware and samples"
                                                        ),
                                                    ],
                                                    style={
                                                        "margin": "8px",
                                                        "paddingLeft": "4px",
                                                        "paddingRight": "4px",
                                                    },
                                                ),
                                            ),
                                        ]
                                    )
                                ],
                                bg="gray.1",
                                style={"whiteSpace": "nowrap"},
                            ),
                            dmc.TableTbody(
                                [
                                    dmc.TableTr(
                                        [
                                            dmc.TableTd(row[0]),
                                            dmc.TableTd(row[1]),
                                            dmc.TableTd(row[2]),
                                            dmc.TableTd(row[3]),
                                            dmc.TableTd(row[4]),
                                            dmc.TableTd(row[5]),
                                        ]
                                    )
                                    for row in TABLE_DEF_PPEL
                                ],
                                fz=12,
                            ),
                        ]
                    ),
                ],
            ),
            dmc.TabsPanel(
                value="samples",
                children=[
                    dmc.Table(
                        [
                            dmc.TableThead(
                                [
                                    dmc.TableTr(
                                        [
                                            dmc.TableTh("Field Name"),
                                            dmc.TableTh("Description"),
                                            dmc.TableTh("Units"),
                                            dmc.TableTh("Data Type"),
                                            dmc.TableTh("Validation"),
                                            dmc.Tooltip(
                                                dmc.TableTh(
                                                    dmc.Flex(
                                                        justify="start",
                                                        align="center",
                                                        gap=0,
                                                        children=[
                                                            "Field Class",
                                                            DashIconify(
                                                                icon="material-symbols-light:indeterminate-question-box-rounded",
                                                                width=24,
                                                                style={
                                                                    "marginLeft": "4px",
                                                                    "marginTop": "2px",
                                                                },
                                                            ),
                                                        ],
                                                    )
                                                ),
                                                label=html.Ul(
                                                    [
                                                        html.Li(
                                                            "RI: required input; used to configure results and calculations within the BioSTAR interface"
                                                        ),
                                                        html.Li(
                                                            "MDO: metadata only; available for documentation purposes but no impact on tool functionality"
                                                        ),
                                                        html.Li(
                                                            "D: derived field; populated by the tool based on current state of hardware and samples"
                                                        ),
                                                    ],
                                                    style={
                                                        "margin": "8px",
                                                        "paddingLeft": "4px",
                                                        "paddingRight": "4px",
                                                    },
                                                ),
                                            ),
                                        ]
                                    )
                                ],
                                bg="gray.1",
                                style={"whiteSpace": "nowrap"},
                            ),
                            dmc.TableTbody(
                                [
                                    dmc.TableTr(
                                        [
                                            dmc.TableTd(row[0]),
                                            dmc.TableTd(row[1]),
                                            dmc.TableTd(row[2]),
                                            dmc.TableTd(row[3]),
                                            dmc.TableTd(row[4]),
                                            dmc.TableTd(row[5]),
                                        ]
                                    )
                                    for row in TABLE_DEF_SAMPLES
                                ],
                                fz=12,
                            ),
                        ]
                    ),
                ],
            ),
        ],
    ),
)

POPUP_DIV = html.Div(
    [
        CONFIGURE_PROJECT_MODAL,
        CONFIGURE_HARDWARE_MODAL,
        CONFIGURE_SAMPLE_MODAL,
        IMPORT_HARDWARE_MODAL,
        IMPORT_SAMPLES_MODAL,
        TABLE_DEFS_MODAL,
    ]
)
