from win10toast import ToastNotifier

CREATE_NO_WINDOW = 0x08000000

common_color = {
    "primary": "color: #007bff;",
    "success": "color: #28a745;",
    "info": "color: #17a2b8;",
    "warning": "color: #ffc107;",
    "danger": "color: #dc3545;"
}

common_font = {
    "bold": "font-weight: bold;",
    "underline": "text-decoration: underline;"
}

font = {
    "title": "font-size: 10pt;",
    "mini_title": "font-size: 8pt;",
    "main_title": "font-size: 16pt;"
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
    "GI": {
        "s": "G.I. URL",
        "l": "Getting Image URL"
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

btns = {
    "default": "border-radius: 6px; min-width: 80px; min-height: 35px; border-color: #007bff; border: 1px solid #007bff;",
    "primary": "color: #fff;background-color: #007bff;border-color: #007bff;",
    "success": "color: #fff;background-color: #28a745;border-color: #28a745;",
    "info": "color: #fff;background-color: #17a2b8;border-color: #17a2b8;",
    "danger": "color: #fff;background-color: #dc3545;border-color: #dc3545;",
    "warning": "color: #fff;background-color: #ffc107;border-color: #ffc107;",
    "outline-primary": "border-color: #007bff; border: 1px solid #007bff; color: #007bff;",
    "outline-success": "border-color: #28a745; border: 1px solid #28a745; color: #28a745;",
    "outline-info": "border-color: #17a2b8; border: 1px solid #17a2b8; color: #17a2b8;",
    "outline-danger": "border-color: #dc3545; border: 1px solid #dc3545; color: #dc3545;",
    "outline-warning": "border-color: #ffc107; border: 1px solid #ffc107; color: #ffc107;",
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
