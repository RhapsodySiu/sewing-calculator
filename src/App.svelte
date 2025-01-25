<script lang="ts">
    import WebGl from "./WebGL.svelte";

  const DIMENSION_LOOKUP = {
    A6: { width: 10.5, height: 14.8 },
    A5: { width: 14.8, height: 21 },
    A4: { width: 21, height: 29.7 },
    B6: { width: 12.5, height: 17.6 },
    B5: { width: 17.6, height: 25 },
    B4: { width: 25, height: 35.3 },
  } as const;

  let dimension = "A6" as keyof typeof DIMENSION_LOOKUP;
  let roundness = 2;
  let thickness = 2;
  let sa = 1;

  let width = DIMENSION_LOOKUP[dimension].width;
  let height = DIMENSION_LOOKUP[dimension].height;
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
        {#each Object.keys(DIMENSION_LOOKUP) as dim}
          <option value={dim}>{dim}</option>
        {/each}
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

<WebGl thickness={thickness} width={width} height={height}></WebGl>

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
