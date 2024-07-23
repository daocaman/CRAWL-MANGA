from win10toast import ToastNotifier

CREATE_NO_WINDOW = 0x08000000

common_color = {
    "primary": "#007bff",
    "success": "#28a745",
    "info": "#17a2b8",
    "warning": "#ffc107",
    "danger": "#dc3545"
}

bg_primary = {
    "background-color": common_color["primary"]
}

bg_success = {
    "background-color": common_color["success"]
}

bg_info = {
    "background-color": common_color["info"]
}

bg_danger = {
    "background-color": common_color["danger"]
}

bg_warning = {
    "background-color": common_color["danger"]
}


text_primary = {
    "color": common_color["primary"]
}

text_success = {
    "color": common_color["success"]
}

text_info = {
    "color": common_color["info"]
}

text_danger = {
    "color": common_color["danger"]
}

text_warning = {
    "color": common_color["warning"]
}

font_bold = {
    "font-weight": "bold"
}

font_underline = {
    "text-decoration": "underline"
}

font_main_title = {
    "font-size": "16pt"
}

font_mini_title = {
    "font-size": "8pt"
}

font_title = {
    "font-size": "10pt"
}

tabs = {
    "RN": {
        "s": "R. Folder",
        "l": "Rename Folder"
    },

    "GC": {
        "s": "G. Chapter",
        'l': "Getting Chapter"
    },
    "DV": {
        "s": "D. Novel",
        "l": "Download Novel"
    },
    "DC": {
        "s": "D.C URL",
        "l": "Download Comic URL"
    },
    "GI": {
        "s": "G.I Comic",
        "l": "Getting Info Comic"
    },
    "AC": {
        "s": "A. Comic",
        "l": "Archive Comic"
    },
}


btn_default = {
    "border-radius": "6px",
    "min-width": "80px",
    "min-height": "24px",
    "color": "#fff"
}

btn_primary = {
    **btn_default,
    "background-color": "#007bff",
    "border-color": "#007bff",
    "border": "1px solid #007bff",
}

btn_success = {
    **btn_default,
    "background-color": "#28a745",
    "border-color": "#28a745",
    "border": "1px solid #28a745",
}

btn_info = {
    **btn_default,
    "background-color": "#17a2b8",
    "border-color": "#17a2b8",
    "border": "1px solid #17a2b8",
}

btn_danger = {
    **btn_default,
    "background-color": "#dc3545",
    "border-color": "#dc3545",
    "border": "1px solid #dc3545",
}

btn_warning = {
    **btn_default,
    "background-color": "#ffc107",
    "border-color": "#ffc107",
    "border": "1px solid #ffc107",
}

btn_outline_primary = {
    **btn_default,
    "border-color": "#007bff",
    "border": "1px solid #007bff",
    "color": "#007bff",
}

btn_outline_success = {
    **btn_default,
    "border-color": "#28a745",
    "border": "1px solid #28a745",
    "color": "#28a745",
}

btn_outline_info = {
    **btn_default,
    "border-color": "#17a2b8",
    "border": "1px solid #17a2b8",
    "color": "#17a2b8",
}

btn_outline_danger = {
    **btn_default,
    "border-color": "#dc3545",
    "border": "1px solid #dc3545",
    "color": "#dc3545",
}

btn_outline_warning = {
    **btn_default,
    "border-color": "#ffc107",
    "border": "1px solid #ffc107",
    "color": "#ffc107",
}

servers_novel = {
    "metruyencv": 0,
    "sstruyen": 1,
    "trumtruyen": 2,
    "truyenfull": 3
}

servers_manga = {
    "nettruyen": 0,
    "mangasee": 1,
    "sinhvien": 2
}

msg = {
    "suc_rn": {"t": "Success", "m": "Rename folder done!!!"},
    "suc_dv": {"t": "Complete", "m": "Download novel done!!!"},
    "err_dv": {"t": "Error", "m": "No internet connection!!!"},
    "suc_gc": {"t": "Success", "m": "Getting link chapter complete!!!"},
    "err_di_er": {"t": "Error", "m": "Something wrong happen!!!"},
    "err_di_401": {"t": "Error", "m": "Missing value or file!!!"},
    "suc_di": {"t": "Success", "m": "Getting image source complete!!!"},
    "suc_dc": {"t": "Success", "m": "Download image complete!!!"},
    "suc_gi": {"t": "Success", "m": "Download comic info complete!!!"},
    "suc_ac": {"t": "Success", "m": "Archive comic complete!!!"},
}

break_chapter_str = "※----*-------⁛-------*----※"


n = ToastNotifier()
