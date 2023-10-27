interface Window {
  readonly GLOBAL_CONFIG: GlobalConfig;
}

type GlobalConfig = {
  readonly CSRF: string;
}