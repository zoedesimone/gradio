<script lang="ts">
	import { onMount } from "svelte";

	export let offsets = [5, 30]; // Initial percentages of each category
	export let isDragging = [false, false]; // Tracks which thumbs are being dragged
	export let categories = ["Red", "Green", "Blue"]; // Labels for each category
	export let bar; // DOM reference to the bar
	export let savedPositions = [...offsets]; // Saved positions
	let keyStep = 1; // Step size for keyboard events

	onMount(() => {
		const onMouseMove = (event) => {
			isDragging.forEach((dragging, index) => {
				if (dragging) {
					let barRect = bar.getBoundingClientRect();
					let newX = event.clientX - barRect.left;
					let newOffset = (newX / barRect.width) * 100;

					newOffset = Math.max(
						newOffset,
						index > 0 ? offsets[index - 1] + 5 : 0
					);
					newOffset = Math.min(
						newOffset,
						index < offsets.length - 1 ? offsets[index + 1] - 5 : 100
					);

					offsets[index] = newOffset;
					savedPositions = [...offsets];
				}
			});
		};

		const onMouseUp = () => {
			isDragging = [false, false];
		};

		window.addEventListener("mousemove", onMouseMove);
		window.addEventListener("mouseup", onMouseUp);

		return () => {
			window.removeEventListener("mousemove", onMouseMove);
			window.removeEventListener("mouseup", onMouseUp);
		};
	});

	function startDrag(index) {
		isDragging[index] = true;
	}

	function keydown(event, index) {
		if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
			event.preventDefault();
			let step = event.key === "ArrowLeft" ? -keyStep : keyStep;
			let newOffset = offsets[index] + step;

			newOffset = Math.max(newOffset, index > 0 ? offsets[index - 1] + 5 : 0);
			newOffset = Math.min(
				newOffset,
				index < offsets.length - 1 ? offsets[index + 1] - 5 : 100
			);

			offsets[index] = newOffset;
		}
	}
</script>

<div class="bar" bind:this={bar}>
	<div class="end-label" style="left: 0%;">0</div>
	<div class="end-label" style="left: 100%;">100</div>
	<div class="section" style="background: red; flex-basis: {offsets[0]}%">
		<span class="text">{categories[0]}</span>
	</div>
	<div
		class="thumb {isDragging[0] ? 'active' : ''}"
		style="left: {offsets[0]}%"
		on:mousedown={() => startDrag(0)}
		on:keydown={(event) => keydown(event, 0)}
		tabindex="0"
		role="slider"
		aria-valuemin="0"
		aria-valuemax="100"
		aria-valuenow={offsets[0]}
		aria-label="Change Red Section Width"
	>
		<div class="thumb-label" style="left: 50%;">{Math.round(offsets[0])}</div>
	</div>
	<div
		class="section"
		style="background: green; flex-basis: {offsets[1] - offsets[0]}%"
	>
		<span class="text">{categories[1]}</span>
	</div>
	<div
		class="thumb {isDragging[1] ? 'active' : ''}"
		style="left: {offsets[1]}%"
		on:mousedown={() => startDrag(1)}
		on:keydown={(event) => keydown(event, 1)}
		tabindex="0"
		role="slider"
		aria-valuemin="0"
		aria-valuemax="100"
		aria-valuenow={offsets[1]}
		aria-label="Change Green Section Width"
	>
		<div class="thumb-label" style="left: 50%;">{Math.round(offsets[1])}</div>
	</div>
	<div
		class="section"
		style="background: blue; flex-basis: {100 - offsets[1]}%"
	>
		<span class="text">{categories[2]}</span>
	</div>
</div>

<p>Thumb positions: {savedPositions.join(", ")}</p>

<style>
	.bar {
		height: 30px;
		display: flex;
		width: 100%;
		position: relative;
		background-color: #ddd;
	}

	.thumb {
		position: absolute;
		width: 10px;
		height: 30px;
		background: #000;
		cursor: col-resize;
		z-index: 10;
	}
	.thumb.active {
		outline-color: white;
		background: white;
		opacity: 1;
	}

	.section {
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #fff;
		text-align: center;
		position: relative;
		padding: 0 5px;
		box-sizing: border-box;
	}

	.text {
		position: absolute;
		width: 100%;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.thumb-label {
		position: absolute;
		transform: translateX(-50%) translateY(-100%);
		white-space: nowrap;
		font-size: 0.8em;
		user-select: none;
	}

	.end-label {
		position: absolute;
		transform: translateX(-50%) translateY(-100%);
		white-space: nowrap;
		font-size: 0.8em;
		user-select: none;
	}
</style>
