<script lang="ts">
    import WebGl from "./WebGL.svelte";

  let dimension = "A6";
  let roundness = 2;
  let thickness = 0.1;
  let sa = 1;
</script>

<main>
  <h1>Sewing calculator</h1>
  <form>
    <div>
      <label for="thickness">Thickness:</label>
      <input type="number" id="thickness" bind:value={thickness} step="0.1" /> cm
    </div>
    <div>
      <label for="dimension">Dimension:</label>
      <select id="dimension" bind:value={dimension}>
        <option value="A6">A6</option>
        <option value="A5">A5</option>
        <option value="A4">A4</option>
      </select>
    </div>
    <div>
      <label for="roundness">Roundness:</label>
      <input type="number" id="roundness" bind:value={roundness} /> cm
    </div>
    <div>
      <label for="sa">SA:</label>
      <input type="number" id="sa" bind:value={sa} /> cm
    </div>
  </form>
</main>

<WebGl thickness={thickness}></WebGl>

<style>
  main {
    font-family: Arial, sans-serif;
    padding: 2em;
  }
  form {
    display: flex;
    flex-direction: column;
    gap: 1em;
  }
  label {
    margin-right: 0.5em;
  }
  div {
    display: flex;
    align-items: center;
  }
  input, select {
    margin-left: 0.5em;
  }
</style>
