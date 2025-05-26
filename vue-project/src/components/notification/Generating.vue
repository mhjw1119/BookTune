<template>
  <span class="generating-flex">
    <span class="generating-text korean-font">음악 생성중</span>
    <span class="my-spinner"></span>
  </span>
</template>

<style>
.generating-flex {
  display: inline-flex;
  align-items: center;
  vertical-align: middle;
}
.generating-text {
  margin-right: 8px;
  font-size: 1.05rem;
  color: #2196F3;
  font-family: 'Gaegu', cursive;
  white-space: nowrap;
}
.my-spinner {
  width: 18px;
  height: 18px;
  border: 3px solid #2196F3;
  border-right: 3px solid transparent;
  border-radius: 50%;
  animation: my-spin 1s linear infinite;
  box-sizing: border-box;
  display: inline-block;
  vertical-align: middle;
}
@keyframes my-spin {
  100% { transform: rotate(360deg); }
}
</style>