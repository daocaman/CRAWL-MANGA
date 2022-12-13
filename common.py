from win10toast import ToastNotifier

common_color = {
    "primiary": "color: #007bff;",
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
    "RN": "Rename Folder",
    "GC": "Getting Chapter",
    "DV": "Download Novel",
    "GI": "Getting image url"
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

msg = {
    "suc_rn": {"t": "Success", "m": "Rename folder done!!!"},
    "suc_dv": {"t": "Complete", "m": "Download novel done!!!"},
    "suc_gc": {"t": "Success", "m": "Getting link chapter complete!!!"},

}


n = ToastNotifier()
