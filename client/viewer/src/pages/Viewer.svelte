<script lang="ts">
    import * as Resizable from "$lib/components/ui/resizable/index.js";
    import { Button } from "../lib/components/ui/button/index.js"
    import * as Card from "../lib/components/ui/card/index.js";
</script>
   
  

<div class = "h-screen dark">
    <header style="" class="sticky top-0 text-center">
        <Card.Root style="border-radius:0px; border:0px; border-color: #00000000;" 
                class ="text-center items-center">
            <Card.Content class="p-3 grid grid-cols-3 gap-0 text-center">
                <div>
                    <Button href="/" class="text-center text-[10px] h-5 w-10" variant="outline">
                        Home
                    </Button>
                </div>
                
                <div class="grid text-center">
                    3D Viewer
                </div>
                <div>
                </div>
            </Card.Content>
        </Card.Root>
    </header>
    <Resizable.PaneGroup direction="horizontal" class=" border">
        <Resizable.Pane defaultSize={35}>
            <Resizable.PaneGroup direction="vertical">
              <Resizable.Pane defaultSize={25}>
                <div class="flex h-full items-center justify-center p-6">
                  <span class="font-semibold">Two</span>
                </div>
              </Resizable.Pane>
              <Resizable.Handle />
              <Resizable.Pane defaultSize={75}>
                <div class="flex h-full items-center justify-center p-6">
                  <span class="font-semibold">Three</span>
                </div>
              </Resizable.Pane>
            </Resizable.PaneGroup>
          </Resizable.Pane>
          <Resizable.Handle />
        <Resizable.Pane defaultSize={50}>
          <div class="flex items-center justify-center p-6">
            <span class="font-semibold">One</span>
          </div>
        </Resizable.Pane>
      </Resizable.PaneGroup>
</div>