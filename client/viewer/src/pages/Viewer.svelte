<script lang="ts">
    import * as Resizable from "$lib/components/ui/resizable/index.js";
    import { Button } from "../lib/components/ui/button/index.js"
    import * as Card from "../lib/components/ui/card/index.js";
    import * as Collapsible from "$lib/components/ui/collapsible/index.js";

    let isOpen = false;
</script>
   


<div class = "h-screen dark">
        <Collapsible.Root open={isOpen}  class ="text-center items-center p-0">   
                <Card.Root style="border-radius:0px; border:0px; border-color: #00000000;" 
                    class ="text-center items-center  p-0">
                    <Collapsible.Content>
                    <Card.Content class="p-0 grid grid-cols-3 gap-0 text-center">
                    <div>
                        <!-- <Button href="/" class="text-center text-[10px] h-5 w-10  p-0" variant="outline">
                            Home
                        </Button> -->
                    </div>
                    
                    <div class="text-center  p-0">
                        <Button href="/" class="p-0" variant="ghosts">
                            3D Viewer
                        </Button>
                        <!-- 3D Viewer -->
                    </div>
                    <div>
                    </div>
                </Card.Content>
                </Collapsible.Content >
                <Card.Footer class="grid gap-0 p-0" >
                        <Collapsible.Trigger asChild class="p-0 text-center items-center">
                            <Button on:click={() => (isOpen = !isOpen)} variant="secondary"
                                class="w-20 h-2 p-0">
                            </Button>
                        </Collapsible.Trigger> 
                </Card.Footer>
            </Card.Root>
    </Collapsible.Root>
    
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

<!-- <style>
    .header {
        background-color: #f8f9fa;
        border-bottom: 1px solid #e9ecef;
        padding: 1rem;
    }
</style> -->