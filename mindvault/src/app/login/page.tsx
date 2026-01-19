"use client";

import { useEffect, useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { z } from "zod";
import { useForm, type Resolver, type SubmitHandler } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";

import {
  CaptchaInfo,
  LoginFormData,
  fetchCaptcha,
  login,
} from "@/lib/api/auth";

const loginSchema = z.object({
  username: z.string().min(1, "请输入用户名"),
  password: z.string().min(1, "请输入密码"),
  captcha: z.string().min(1, "请输入验证码"),
  remember: z.boolean(),
});

type LoginSchema = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const [captcha, setCaptcha] = useState<CaptchaInfo | null>(null);
  const [loadingCaptcha, setLoadingCaptcha] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const form = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema) as Resolver<LoginSchema>,
    defaultValues: {
      username: "",
      password: "",
      captcha: "",
      remember: false,
    },
  });

  const loadCaptcha = async () => {
    try {
      setLoadingCaptcha(true);
      setError(null);
      const data = await fetchCaptcha();
      setCaptcha(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "获取验证码失败");
    } finally {
      setLoadingCaptcha(false);
    }
  };

  useEffect(() => {
    void loadCaptcha();
  }, []);

  const onSubmit: SubmitHandler<LoginSchema> = (values) => {
    if (!captcha) {
      setError("验证码加载中，请稍后重试");
      return;
    }

    const payload: LoginFormData = {
      username: values.username,
      password: values.password,
      captcha: values.captcha,
      captcha_key: captcha.key,
      remember: values.remember,
      login_type: "PC端",
    };

    setError(null);

    startTransition(async () => {
      try {
        await login(payload);
        // 登录成功，跳转首页
        router.push("/");
      } catch (e) {
        setError(e instanceof Error ? e.message : "登录失败，请稍后重试");
        // 刷新验证码
        void loadCaptcha();
        form.setValue("captcha", "");
      }
    });
  };

  const captchaImgSrc =
    captcha && captcha.img_base
      ? captcha.img_base.startsWith("data:image")
        ? captcha.img_base
        : `data:image/png;base64,${captcha.img_base}`
      : "";

  return (
    <div className="flex min-h-screen items-center justify-center bg-linear-to-br from-slate-900 via-slate-950 to-slate-900 px-4">
      <Card className="w-full max-w-md border-slate-800 bg-slate-900/60 text-slate-50 shadow-xl shadow-slate-900/40 backdrop-blur">
        <CardHeader className="space-y-2 text-center">
          <CardTitle className="text-2xl font-semibold tracking-tight">
            欢迎登录 MindVault
          </CardTitle>
          <p className="text-sm text-slate-400">
            请输入账号、密码与验证码进入系统
          </p>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form
              onSubmit={form.handleSubmit(onSubmit)}
              className="space-y-6"
            >
              <FormField
                control={form.control}
                name="username"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>用户名</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="请输入用户名"
                        autoComplete="username"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>密码</FormLabel>
                    <FormControl>
                      <Input
                        type="password"
                        placeholder="请输入密码"
                        autoComplete="current-password"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="captcha"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>验证码</FormLabel>
                    <div className="flex items-start gap-3">
                      <FormControl>
                        <Input
                          placeholder="请输入验证码"
                          autoComplete="one-time-code"
                          {...field}
                        />
                      </FormControl>
                      <div className="flex flex-col gap-1">
                        <button
                          type="button"
                          onClick={() => void loadCaptcha()}
                          className="group relative flex h-9 min-w-[96px] items-center justify-center overflow-hidden rounded-md border border-slate-700 bg-slate-900/70 transition hover:border-sky-500/70 hover:bg-slate-900"
                        >
                          {loadingCaptcha ? (
                            <div className="flex h-full w-full items-center justify-center gap-2 text-xs text-slate-300">
                              <Spinner className="h-4 w-4" />
                              刷新中...
                            </div>
                          ) : captchaImgSrc ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img
                              src={captchaImgSrc}
                              alt="验证码"
                              className="h-9 w-auto max-w-[160px] object-contain"
                            />
                          ) : (
                            <span className="text-xs text-slate-300">
                              点击获取验证码
                            </span>
                          )}
                          <div className="pointer-events-none absolute inset-0 bg-linear-to-tr from-sky-500/0 via-sky-500/10 to-sky-500/0 opacity-0 blur-md transition group-hover:opacity-100" />
                        </button>
                        <span className="text-[11px] text-slate-400">
                          看不清？点击图片刷新
                        </span>
                      </div>
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="remember"
                render={({ field }) => (
                  <FormItem className="flex items-center gap-2 space-y-0">
                    <FormControl>
                      <Checkbox
                        checked={field.value}
                        onCheckedChange={(checked) =>
                          field.onChange(checked === true)
                        }
                      />
                    </FormControl>
                    <FormLabel className="font-normal text-slate-300">
                      记住我
                    </FormLabel>
                  </FormItem>
                )}
              />

              {error && (
                <div className="rounded-md border border-red-500/40 bg-red-500/10 px-3 py-2 text-xs text-red-200">
                  {error}
                </div>
              )}

              <Button
                type="submit"
                className="inline-flex w-full items-center justify-center gap-2 bg-sky-500 text-slate-950 hover:bg-sky-400"
                disabled={isPending}
              >
                {isPending && <Spinner className="h-4 w-4" />}
                {isPending ? "登录中..." : "登录"}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}


