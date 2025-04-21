<script lang="ts">
    import "../app.css"
    // Import necessary ShadCN components
    import { Button } from "../lib/components/ui/button/index.js"
    // import { Input } from "../lib/components/ui/input/index.js"
    import * as Card from "../lib/components/ui/card/index.js";
    // import { Content } from "node_modules/bits-ui/dist/bits/accordion/exports.js";

    import * as djauth from "../lib/hooks/django-auth.js";

    let divs = [...Array(5).keys()];

</script>



<div class="flex flex-col h-screen text-center dark">
    <header style="" class="sticky top-0 text-center">
        <Card.Root style="border-radius:0px; border:0px; border-color: #00000000;" 
                class ="text-center items-center">
            <Card.Content class="p-3 grid grid-cols-3 gap-0 text-center">
                <div></div>
                <div class="grid text-center text-[18px]">
                    3D Viewer
                </div>
                <div>
                    {#if (! djauth.isAuthenticated())}
                        <!-- <div class="flex"> -->
                            
                        <Button href="/login" class="text-center text-[14px] h-7 w-16" variant="outline">
                            Login
                        </Button>
                        
                        <!-- </div> -->
                    {:else}
                    <div>
                        <Button href="/viewer" class="text-center text-[14px] h-7 w-16" variant="outline">
                            Begin
                        </Button>
                    
                        <Button onclick={djauth.logout} href="/" class="text-center text-[14px] h-7 w-16" variant="outline">
                            Logout
                        </Button>
                    </div>
                    {/if}
                </div>
            </Card.Content>
        </Card.Root>
    </header>
    
    {#each { length: 80 }, rank}
        <div>{rank}</div>
    {/each}
</div>
