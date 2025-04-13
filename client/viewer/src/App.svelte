<script lang="ts">
  import "./app.css";
  import Login from "./pages/Login.svelte" 
  import MainPage from "./pages/MainPage.svelte"
  import Viewer from "./pages/Viewer.svelte"
  import { Router, Link, Route } from "svelte-routing"
 
  export let url = "";
</script>



<main> 
  <Router {url}>
    <div>
      <Route path="/viewer" ><Viewer/> </Route>
      <Route path="/login" ><Login/> </Route>
      <Route path="/"><MainPage></MainPage></Route>
    </div>
  </Router>  
</main>

<style>
  main {
    overflow: auto;
    background: linear-gradient(to right,#222222, #222230, #222222 );
    color: #E0E0E0;
  }
</style>
