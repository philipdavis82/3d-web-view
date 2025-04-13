<script lang="ts">
    import "../app.css";
    // import { useForm, validators, HintGroup, Hint, email, required } from "svelte-use-form@latest";
    import { Button } from "../lib/components/ui/button";
    import * as Card from "../lib/components/ui/card/index.js";
  
    import { Input } from "../lib/components/ui/input/index.js";
    import Label from "../lib/components/ui/label/label.svelte";
    
    let pass = $state("");
    let usrn = $state("");
  
    function submit(data:any) {
      console.log(usrn,pass)
    }

    function cancel(data:any) {
      pass = ""
      usrn = ""
      console.log(usrn,pass)
      window.location.href = "/";
    }

</script>



<div class="dark login">
    <div>
      <Card.Root class="w-[380px]">
        <div class="text-center">
          <Card.Header>
            Login
          </Card.Header>
        </div>
        <Card.Content class="grid gap-2">
          <Input bind:value={usrn}
            id="username" 
            placeholder="username" 
            name="username" 
            type="username" />
          
          <Input bind:value={pass}
            placeholder="password" 
            name="password" 
            type="password" />
        
          <div class="grid grid-cols-2 gap-2">
            <Button onclick={submit}> Login </Button>
            <Button onclick={cancel} > Cancel </Button>
          </div>
        </Card.Content>  
        </Card.Root>  
      </div>
    <div>
  </div>
</div>


<style>
    .login  {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
</style>