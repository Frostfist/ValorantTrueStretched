import flet as ft
from assets.modules.core import Config, Resolution


def main(page: ft.Page):
    def on_resize(e):
        cfg.window_width = page.window_width
        cfg.window_height = page.window_height
    
    cfg = Config()

    page.fonts = cfg.fonts
    page.window_height = cfg.window.height
    page.window_width = cfg.window.width
    page.window_max_width = cfg.window.max_width
    page.window_max_height = cfg.window.max_height
    page.window_resizable = cfg.window.resizable
    page.window_min_width = cfg.window.min_width
    page.window_min_height = cfg.window.min_height
   
    root : ft.Ref[ft.Column] = ft.Ref[ft.Column]()
    search_bar : ft.Ref[ft.SearchBar] = ft.Ref[ft.SearchBar]()

    def close_search_bar(e):
        search_bar.current.close_view(e.control.data)

    def remove_resolution(e):
        cfg.resolutions.remove(e.control.data["Value"])
        search_bar.current.controls.pop(e.control.data["Index"])
        search_bar.current.close_view()
        search_bar.current.open_view()
        page.update()


    def add_resolution(e):
        value : str = search_bar.current.value
        
        resolution = Resolution(value)
        
        if resolution not in cfg.resolutions:
            cfg.resolutions.append(resolution)
            search_bar.current.controls.append(ft.ListTile(
                            title=ft.Text(value=resolution),
                            trailing=ft.PopupMenuButton(
                                icon=ft.icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Remove", icon=ft.icons.REMOVE_CIRCLE, on_click=remove_resolution, data={
                                        "Index": cfg.resolutions.index(resolution),
                                        "Value": resolution
                                                                                                                                   })
                                ],
                            ),
                            on_click=close_search_bar,
                            data=search_bar.current.value
                        ))
            search_bar.current.update()



    def apply_resolution(e):
        pass
    
    def reset(e):
        pass


    def on_route_change(route):
        page.views.clear()
       
        page.views.append( 
            ft.View(
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                route="/",
                controls=[
                    ft.Row(ref=root, alignment=ft.MainAxisAlignment.CENTER),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.ElevatedButton(text="Reset", on_click=reset, tooltip="Reset all actions"),
                                    ft.ElevatedButton(text="Add", icon=ft.icons.ADD_TO_PHOTOS, on_click=add_resolution, tooltip="Add resolution to search bar list"),
                                    ft.ElevatedButton(text="Apply", on_click=apply_resolution, tooltip="Apply the search bar resolution")
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                ],
                bottom_appbar=ft.BottomAppBar(
                    shape=ft.NotchShape.CIRCULAR,
                )
            )
        )

        if(page.route == "/"):
            if root != None:
                if cfg.search:
                    root.current.controls = [
                        ft.SearchBar(ref=search_bar, view_hint_text="Choose resolution", height=50, width=cfg.window.min_width)
                    ]

        page.update()
    

    page.on_resize = on_resize
    page.on_route_change = on_route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(main, assets_dir="assets")
