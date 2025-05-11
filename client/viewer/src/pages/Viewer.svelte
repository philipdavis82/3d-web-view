<script lang="ts">
  import * as Resizable from "$lib/components/ui/resizable/index.js";
  import { Button } from "../lib/components/ui/button/index.js";
  import * as Card from "../lib/components/ui/card/index.js";
  import * as Collapsible from "$lib/components/ui/collapsible/index.js";
  import { cn } from "$lib/utils";
  import * as djauth from "../lib/hooks/django-auth.js";
  import * as djquery from "../lib/hooks/django-query.js";
  
  import ScrollArea from "$lib/components/ui/scroll-area/scroll-area.svelte";
  let isOpen = $state(true);

  if (djauth.isAuthenticated()) {
    console.log("Login successful");
  } else {
    console.log("Login failed");
    // window.location.href = "http://localhost:5173/login";
  }

  let CurrentDirectory:Array<any> = $state([]);
  let CurrentDirectoryID = $state(0);
  let LastDirectoryIDs:Array<number>   = [];
  let CurrentFiles:Array<any> = $state([]);
  let CurrentFilesID:number = 0;
  async function topLevel() {
    let dirid = LastDirectoryIDs.pop();
    if(dirid === undefined) {
      dirid = 0;
    }
    const response = await djquery.getDirectories(dirid);
    await getFiles(dirid);
    console.log("Response:", response);
    CurrentDirectory = response.results;
    CurrentDirectoryID = dirid;
  };

  async function nextLevel(id:number) {
    LastDirectoryIDs.push(CurrentDirectoryID);
    const response = await djquery.getDirectories(id);
    console.log("Response:", response);
    CurrentDirectory = response.results;
    CurrentDirectoryID = id;
  };

  async function getFiles(id:number) {
    if(CurrentFilesID == id) return;
    const response = await djquery.getSTLs(id);
    console.log("Response:", response);
    CurrentFiles = response.results;
    CurrentFilesID = id;
  };

  let MainFile: any = $state({
    name: "No file selected",
    path: "",
    id: -1,
  });
  async function setAsMainFile(file:any) {
    // console.log("Setting as main file:", file);
    MainFile = file;
  };

  topLevel();

  // import { slide } from "svelte/transition";
  // import { quintOut } from "svelte/easing";
  import Turntable from "$lib/components/3d/Turntable.svelte";
  import {Canvas} from "@threlte/core";
  
</script>

<div class="h-screen dark flex flex-col">
  <Collapsible.Root open={isOpen} class="text-center items-center p-0">
    <Card.Root
      style="border-radius:0px; border:0px; border-color: #00000000;"
      class="text-center items-center p-0"
    >
      <Card.Content class="p-0 grid grid-cols-3 gap-0 text-center align-middle">
        <div class="text-left pl-2 pt-1">
          <Collapsible.Trigger asChild class="p-0 text-center items-center">
            <Button
              onclick={() => {isOpen = !isOpen;}}
              variant="secondary"
              class="w-8 h-8 p-0"
              style="border-radius:3pt; border-width:1px;"
            >
            
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" 
              style="width: 80%; height: 80%; display: block; align-items: center; justify-content: center;">
                <path fill="white" stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
              </svg>
              
            </Button>
          </Collapsible.Trigger>
        </div>
        <div class="text-center p-0">
          <Button href="/" style="border-radius:2px" class="p-0 text-[18px] h-11 w-30" variant="ghost">3D Viewer</Button>
        </div>
        <div class="text-right pr-5 pt-2">
          <Button
            onclick={djauth.logout}
            href="/"
            class="text-center text-[14px] h-7 w-16"
            variant="outline"
          >
            Logout
          </Button>
          <div></div>
        </div></Card.Content
      >
      <Collapsible.Content class="CollapsibleContent">
        <Card.Footer style="border-top-width: .5mm;" class="grid text-center align-middle p-0 h-full border-solid border-t-[#252525] ">
          <div class="align-middle p-0 ">Test tests tests</div>
        </Card.Footer>
      </Collapsible.Content>
    </Card.Root>
  </Collapsible.Root>
  <Resizable.PaneGroup direction="horizontal" class="border">
    <Resizable.Pane defaultSize={20}>
      <Resizable.PaneGroup direction="vertical">
        <Resizable.Pane defaultSize={100}  class="flex flex-col justify-center items-top p-6">
          
          <Button onclick={topLevel}>Back {CurrentDirectoryID}</Button>
          <div class="flex flex-row justify-center h-full">
            <ScrollArea class="flex-1 justify-start items-top p-6 border">
                <span class="font-semibold">
                  {#each CurrentDirectory as item, index}
                    <div class="listItem">
                      <Button variant="ghost" onclick={()=>{nextLevel(item.id);getFiles(item.id)}}>{index + 1}. {item.name}</Button>
                    </div>
                  {/each}
                </span>
            </ScrollArea>
            <ScrollArea class="flex-1 justify-start items-top p-6 border">
              <span class="font-semibold">
                {#each CurrentFiles as item, index}
                  <div class="listItem">
                    <Button variant="ghost" onclick={()=>{setAsMainFile(item)}}>{index + 1}. {item.name}</Button>
                  </div>
                {/each}
              </span>
          </ScrollArea>
          </div>
        </Resizable.Pane>
        <Resizable.Handle />
        <Resizable.Pane defaultSize={20}>
          <div class="flex h-full items-center justify-center p-6">
            <span class="font-semibold">Three</span>
          </div>
        </Resizable.Pane>
      </Resizable.PaneGroup>
    </Resizable.Pane>
    <Resizable.Handle />
    <Resizable.Pane defaultSize={50}>
      <div class="flex flex-col w-full h-full items-center justify-center p-6">
          <div>
            {MainFile.name}
          </div>
          <div>
            {MainFile.path}
          </div>
          <!-- 3D DIV MOVE TO COMPONENT LIB -->
          <div class="flex-1 w-full h-full items-center justify-center p-6 border">
            <!-- <<span class="font-semibold">3D Viewer</span>> -->
          <Canvas>
            <Turntable/>
          </Canvas>
        </div>
          <!-- 3D DIV MOVE TO COMPONENT LIB -->
      </div>
    </Resizable.Pane>
  </Resizable.PaneGroup>
</div>

