<script lang="ts">
  import WebGl from "./WebGL.svelte";

  const DIMENSION_LOOKUP = {
    A6: { width: 10.5, height: 14.8 },
    A5: { width: 14.8, height: 21 },
    A4: { width: 21, height: 29.7 },
    B6: { width: 12.5, height: 17.6 },
    B5: { width: 17.6, height: 25 },
    B4: { width: 25, height: 35.3 },
    Square: { width: 10, height: 8 },
    Passport: { width: 8.8, height: 12.5 },
    Mini: { width: 5, height: 6 },
  } as const;

  const SPACING = 2;

  let dimension = $state("A6") as keyof typeof DIMENSION_LOOKUP;
  let roundness = $state(2);
  let thickness = $state(2);
  let seamAllowance = $state(1);
  let fabricColor = $state("#3C89C2");
  let zipperColor = $state("#CFD8D8");

  let width = $derived(DIMENSION_LOOKUP[dimension].width + SPACING);
  let height = $derived(DIMENSION_LOOKUP[dimension].height + SPACING * 2);

  function generate() {
    // Empty handler
  }
</script>

<main>
  <h1>Sewing calculator</h1>
  <p>
    This tool helps you generate a sewing pattern for a pouch based on the
    dimensions you provide.
  </p>
  <form>
    <div class="form-row">
      <label for="thickness">Thickness:</label>
      <input type="number" id="thickness" bind:value={thickness} step="0.1" /> cm
    </div>
    <div class="form-row">
      <label for="dimension">Dimension:</label>
      <select id="dimension" bind:value={dimension}>
        {#each Object.keys(DIMENSION_LOOKUP) as dim}
          <option value={dim}>{dim}</option>
        {/each}
      </select>
    </div>
    <div class="form-row">
      <label for="roundness">Roundness:</label>
      <input
        type="number"
        min="0"
        max="5"
        id="roundness"
        bind:value={roundness}
      /> cm
    </div>
    <section>
      <h2>Preview config</h2>
      <div class="form-row">
      <label for="fabricColor">Fabric color:</label>
      <input type="color" id="fabricColor" bind:value={fabricColor} />
      </div>
      <div class="form-row">
      <label for="zipperColor">Zipper color:</label>
      <input type="color" id="zipperColor" bind:value={zipperColor} />
      </div>
    </section>

    <section>
      <h2>Pattern config</h2>
      <div class="form-row">
        <label for="seamAllowance">Seam allowance:</label>
        <input type="number" id="seamAllowance" bind:value={seamAllowance} step="0.1" /> cm
      </div>
    </section>
    <div class="form-row">
      <button type="button" onclick={generate} class="generate-button"
        >Generate</button
      >
    </div>
  </form>
</main>

<p>Preview</p>
<WebGl
  {thickness}
  {width}
  {height}
  {roundness}
  colors={[fabricColor, zipperColor]}
></WebGl>

<style>
  main {
    font-family: Arial, sans-serif;
    padding: 2em;
  }
  form {
    display: grid;
    gap: 1em;
    max-width: 400px;
    margin: auto;
  }

  .form-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  label {
    width: 100px;
    text-align: left;
    padding-right: 1em;
  }

  input[type="number"],
  input[type="color"],
  select {
    flex: 2;
    padding: 0.5em;
    box-sizing: border-box;
  }

  .generate-button {
    background-color: #ecb9bf;
    color: black;
    padding: 10px 20px;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    font-size: 16px;
  }

  .generate-button:hover {
    background-color: #b37291;
  }
</style>
