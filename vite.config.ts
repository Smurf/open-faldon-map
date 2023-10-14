import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, searchForWorkspaceRoot } from 'vite';
import {isoImport } from 'vite-plugin-iso-import';
export default defineConfig({
	server:{
		fs: {
			allow: [
				searchForWorkspaceRoot(process.cwd())			]
		}
	},
	plugins: [sveltekit(), isoImport()]
});
