# Web Audio Recorder

## Usage

```
npm install
npm run start:dev
```

## How To Use

3 Key Steps
1. Select a `Song` from list 
2. Sing along to a `Snipet` of the `Song`
3. Transposed Song is Now Ready

### 1. Select a `Song`
- **[Website]** Send `GET` request to `/songlist` to retrieve list of songs in `<Title, Author>`
- **[Server]** Iterate though `src/data` folder to create a list of `MP3` or `WAV` which is sent to `Client`
- **[Website]** Populate `DOM` with `HTML Objects`
- **[User]** Select Song
- **[Website]** Send `GET` request to `/songlist/<title>/<author>` to retrieve `audio data` of snipet of `Song` in `base64`
- **[Server]** Use `<title>` & `<author>` to retrieve desired snipet 
- ***Proceed to Step 2***

### 2. Sing along to `Snipet`
- **[Website]** Create `<audio>` element with song snipet
- **[User]** Listen and Start singing along
- **[Website]** Records User's voice upon `Start` till `Stop`
- **[Website -> Webworker]** Convert `WebM` to `WAV`
- **[Website]** Send POST request to `/analyse/<title>/<author>` with `WAV` file  in `base64` for `Server` to analyse 
- !! Not done !! **[Server]** Analyse recording to find key and how much to transpose
- **[Server]** Transpose original song and return `Transposed Song`
- ***Proceed to Step 3***

### 3. Transposed song Ready
- **[Website]** Client receive Transposed Song Data in `base64` and create a new `<audio>` tag and `<a>` download link
- **[User]** Sing along or Download song

## Folder Structure 

- `app` : Where all the js, css, html goes 
- `app/dist` : Distribution files are
- `app/build` : Build files, including all JS scripts
- `app/src` : Src files for front end

- `Server` : Server side code