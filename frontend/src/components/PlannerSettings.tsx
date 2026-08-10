import { useEffect, useRef, useState } from "react";

import { clearPlanner, getPlanner, savePlanner, type PlannerSettings as PlannerConfig } from "../api/planner";

function displaySuffix(maskedSuffix: string | null): string | null {
  return maskedSuffix?.replace(/^\.\.\./, "…") ?? null;
}

export function PlannerSettings() {
  const apiKeyRef = useRef<HTMLInputElement>(null);
  const [settings, setSettings] = useState<PlannerConfig | null>(null);
  const [baseUrl, setBaseUrl] = useState("");
  const [model, setModel] = useState("");
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState(false);
  const [action, setAction] = useState<"save" | "clear" | null>(null);
  const [actionError, setActionError] = useState<"save" | "clear" | null>(null);
  const settingsVersion = useRef(0);

  useEffect(() => {
    let active = true;
    const version = settingsVersion.current;

    getPlanner().then((loaded) => {
      if (!active || settingsVersion.current !== version) return;
      setSettings(loaded);
      setBaseUrl(loaded.baseUrl);
      setModel(loaded.model);
    }).catch(() => {
      if (active && settingsVersion.current === version) setLoadError(true);
    }).finally(() => {
      if (active) setLoading(false);
    });

    return () => { active = false; };
  }, []);

  function applySettings(next: PlannerConfig) {
    setSettings(next);
    setBaseUrl(next.baseUrl);
    setModel(next.model);
  }

  async function save(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const apiKey = apiKeyRef.current?.value ?? "";
    settingsVersion.current += 1;
    setAction("save");
    setActionError(null);
    setLoadError(false);
    try {
      applySettings(await savePlanner({ baseUrl, model, apiKey }));
    } catch {
      setActionError("save");
    } finally {
      if (apiKeyRef.current) apiKeyRef.current.value = "";
      setAction(null);
    }
  }

  async function clear() {
    settingsVersion.current += 1;
    setAction("clear");
    setActionError(null);
    setLoadError(false);
    try {
      applySettings(await clearPlanner());
    } catch {
      setActionError("clear");
    } finally {
      if (apiKeyRef.current) apiKeyRef.current.value = "";
      setAction(null);
    }
  }

  const disabled = loading || action !== null;
  const suffix = displaySuffix(settings?.maskedSuffix ?? null);

  return (
    <section className="panel" aria-labelledby="planner-heading">
      <h2 id="planner-heading">Planner 配置</h2>
      {loading && !settings ? <p className="state-message">正在加载 Planner 配置…</p> : null}
      {loadError ? <p className="state-message state-message--error">无法加载 Planner 配置</p> : null}
      {!loadError && settings ? <p>状态：{settings.configured ? <span>已配置{suffix ? <>（密钥后缀：<span>{suffix}</span>）</> : null}</span> : <span>尚未配置</span>}</p> : null}
      {actionError ? <p className="state-message state-message--error">{actionError === "save" ? "无法保存 Planner 配置" : "无法清除 Planner 配置"}</p> : null}
      <form className="settings-form" onSubmit={save}>
        <label>
          Planner 地址
          <input type="url" value={baseUrl} disabled={disabled} onChange={(event) => setBaseUrl(event.target.value)} />
        </label>
        <label>
          模型
          <input value={model} disabled={disabled} onChange={(event) => setModel(event.target.value)} />
        </label>
        <label>
          API 密钥
          <input ref={apiKeyRef} type="password" disabled={disabled} autoComplete="off" />
        </label>
        <div className="panel-actions">
          <button type="submit" disabled={disabled}>保存 Planner 配置</button>
          <button type="button" disabled={disabled} onClick={clear}>清除 Planner 配置</button>
        </div>
      </form>
    </section>
  );
}
