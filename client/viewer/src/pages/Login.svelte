<script lang="ts">
    import "../app.css";
    // import { useForm, validators, HintGroup, Hint, email, required } from "svelte-use-form@latest";
    import { Button } from "../lib/components/ui/button";
    import * as Card from "../lib/components/ui/card/index.js";
  
    import { Input } from "../lib/components/ui/input/index.js";
    import Label from "../lib/components/ui/label/label.svelte";
    import Viewer from "./Viewer.svelte";
    
    import * as djauth from "../lib/hooks/django-auth.js";

    let pass = $state("");
    let usrn = $state("");
  
    async function submit(data:any) {
      console.log(usrn,pass);
      
      await djauth.authenticateWithDjango("http://127.0.0.1:8000", usrn, pass);
      let table = {
        headers: djauth.addAuthHeader({
          'Content-Type': 'application/json'
        })
      };

      if(djauth.isAuthenticated()){
        console.log("Login successful");
        window.location.href = "/viewer";
        // window.location.href = "http://localhost:5173/login"
      } else {
        console.log("Login failed");
        alert("Invalid username or password");
      }

      // if (usrn == "admin" && pass == "admin") {
      //   console.log("Login successful");
      //   window.location.href = "/viewer";
      // } else {
      //   console.log("Login failed");
      //   alert("Invalid username or password");
      // }
      // window.location.href = "/viewer";
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