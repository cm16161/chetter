import AcmeLogo from '@/app/ui/acme-logo';
import { ArrowRightIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import styles from '@/app/ui/home.module.css';
import { lusitana  } from "@/app/ui/fonts.ts"
import Image from 'next/image';

export default function Page() {
  return (
    <main className="flex min-h-screen flex-col p-6">
      <div className="flex h-20 shrink-0 items-end rounded-lg bg-fuchsia-400 p-4 md:h-52">
        { <AcmeLogo /> }
      </div>
      <div className="mt-4 flex grow flex-col gap-4 md:flex-row">
        <div className="flex flex-col justify-center gap-6 rounded-lg bg-gray-50 px-6 py-10 md:w-2/5 md:px-20">
      <div
        className={styles.shape}
            />
          <p className={`${lusitana.className} text-xl text-gray-800 md:text-3xl md:leading-normal antialiased`}>
            <strong>Welcome to Chetter.</strong></p>
          <p>
            This is an <a className="line-through">(X)</a> Twitter clone.
          </p>
          <p> We use <strong>AI</strong> (Ananya & Ishan) to revolutionize social media</p>
          <p> We hope you enjoy using this as much as we did making it <strong>(Read: Not a lot)</strong></p>
          <Link
            href="/dashboard/feed"
            className="flex items-center gap-5 self-start rounded-lg bg-fuchsia-400 px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-fuchsia-400 md:text-base"
          >
            <span>Log in</span> <ArrowRightIcon className="w-5 md:w-6" />
          </Link>
        </div>
        <div className="flex items-center justify-center p-6 md:w-3/5 md:px-28 md:py-12">
          {/* Add Hero Images Here */}
        </div>
      </div>
    </main>
  );
}
