window.trame.utils.file_loading = {
    actions: {
        async send_chunk(files, upload_chunk_method_name) {
            const files_array = Array.from(files)
            if (files === undefined) {{
              return;
            }}

            const chunk_size = 100;
            for (let offset = 0; offset < files.length; offset += chunk_size) {{
              const chunk = files_array.slice(offset, offset+chunk_size);
              await trame.trigger(upload_chunk_method_name, [chunk])
            }}
            await trame.trigger(upload_chunk_method_name, [[]]);
        },
    },
}